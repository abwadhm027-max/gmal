import { useState } from "react";
import { Alert, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";
import { router } from "expo-router";
import { signIn } from "../lib/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    try {
      setBusy(true);
      await signIn(email, password);
      router.replace("/home");
    } catch (e: any) {
      Alert.alert("خطأ", e?.message ?? "تعذر تسجيل الدخول");
    } finally {
      setBusy(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.box}>
        <Text style={styles.logo}>IraqJobs</Text>
        <Text style={styles.heading}>تسجيل الدخول</Text>
        <TextInput value={email} onChangeText={setEmail} placeholder="البريد الإلكتروني" autoCapitalize="none" keyboardType="email-address" style={styles.input} />
        <TextInput value={password} onChangeText={setPassword} placeholder="كلمة المرور" secureTextEntry style={styles.input} />
        <Pressable style={styles.button} onPress={submit} disabled={busy}>
          <Text style={styles.buttonText}>{busy ? "جارٍ الدخول..." : "دخول"}</Text>
        </Pressable>
        <Pressable onPress={() => router.push("/register")}>
          <Text style={styles.link}>إنشاء حساب جديد</Text>
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
  buttonText: { color: "#fff", fontWeight: "700" },
  link: { textAlign: "center", marginTop: 18, fontWeight: "700" }
});
