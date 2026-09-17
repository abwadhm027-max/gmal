import { useState } from "react";
import { Alert, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";
import { router } from "expo-router";
import { signUp } from "../lib/auth";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (!name.trim() || !email.trim() || password.length < 6) {
      Alert.alert("تنبيه", "املأ البيانات بشكل صحيح، وكلمة المرور 6 أحرف على الأقل.");
      return;
    }
    try {
      setBusy(true);
      await signUp(email, password, name);
      Alert.alert("تم", "تم إنشاء الحساب. إذا طلب منك تأكيد البريد، أكده ثم سجل الدخول.");
      router.replace("/login");
    } catch (e: any) {
      Alert.alert("خطأ", e?.message ?? "تعذر إنشاء الحساب");
    } finally {
      setBusy(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.box}>
        <Text style={styles.logo}>IraqJobs</Text>
        <Text style={styles.heading}>إنشاء حساب</Text>
        <TextInput value={name} onChangeText={setName} placeholder="الاسم الكامل" style={styles.input} />
        <TextInput value={email} onChangeText={setEmail} placeholder="البريد الإلكتروني" autoCapitalize="none" keyboardType="email-address" style={styles.input} />
        <TextInput value={password} onChangeText={setPassword} placeholder="كلمة المرور" secureTextEntry style={styles.input} />
        <Pressable style={styles.button} onPress={submit} disabled={busy}>
          <Text style={styles.buttonText}>{busy ? "جارٍ الإنشاء..." : "إنشاء الحساب"}</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", backgroundColor: "#f5f6f8" },
  box: { margin: 20, padding: 22, backgroundColor: "#fff", borderRadius: 18 },
  logo: { fontSize: 30, fontWeight: "800", textAlign: "center" },
  heading: { fontSize: 22, fontWeight: "700", textAlign: "right", marginVertical: 20 },
  input: { borderWidth: 1, borderColor: "#ddd", borderRadius: 12, padding: 14, marginBottom: 12, textAlign: "right" },
  button: { backgroundColor: "#111", padding: 15, borderRadius: 12, alignItems: "center" },
  buttonText: { color: "#fff", fontWeight: "700" }
});
