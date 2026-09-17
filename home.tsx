import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  View
} from "react-native";
import { getJobs, Job } from "../lib/jobs";

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadJobs(value = "") {
    try {
      setError("");
      setLoading(true);
      setJobs(await getJobs(value));
    } catch (e: any) {
      setError(e?.message ?? "حدث خطأ");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadJobs();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>IraqJobs</Text>
        <Text style={styles.subtitle}>وظائف العراق</Text>
      </View>

      <TextInput
        value={search}
        onChangeText={setSearch}
        onSubmitEditing={() => loadJobs(search)}
        placeholder="ابحث عن وظيفة، شركة أو مدينة"
        style={styles.search}
        textAlign="right"
      />

      <Pressable style={styles.button} onPress={() => loadJobs(search)}>
        <Text style={styles.buttonText}>بحث</Text>
      </Pressable>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      {loading ? (
        <ActivityIndicator size="large" style={{ marginTop: 30 }} />
      ) : (
        <FlatList
          data={jobs}
          keyExtractor={(item) => item.id}
          contentContainerStyle={{ padding: 16 }}
          ListEmptyComponent={
            <Text style={styles.empty}>لا توجد وظائف حالياً.</Text>
          }
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.title}>{item.title}</Text>
              <Text style={styles.company}>{item.company}</Text>
              <Text style={styles.city}>📍 {item.city}</Text>
              {item.salary_min || item.salary_max ? (
                <Text style={styles.salary}>
                  💰 {item.salary_min ?? "—"} - {item.salary_max ?? "—"} د.ع
                </Text>
              ) : null}
              <Text style={styles.description} numberOfLines={3}>
                {item.description}
              </Text>
            </View>
          )}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f5f6f8" },
  header: { padding: 20, alignItems: "flex-end" },
  logo: { fontSize: 30, fontWeight: "800" },
  subtitle: { color: "#666", marginTop: 4 },
  search: {
    backgroundColor: "#fff",
    marginHorizontal: 16,
    padding: 15,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#ddd"
  },
  button: {
    margin: 16,
    marginTop: 10,
    padding: 14,
    borderRadius: 12,
    backgroundColor: "#111",
    alignItems: "center"
  },
  buttonText: { color: "#fff", fontWeight: "700", fontSize: 16 },
  card: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 18,
    marginBottom: 12
  },
  title: { fontSize: 20, fontWeight: "800", textAlign: "right" },
  company: { marginTop: 7, fontWeight: "600", textAlign: "right" },
  city: { marginTop: 6, color: "#555", textAlign: "right" },
  salary: { marginTop: 6, textAlign: "right" },
  description: { marginTop: 10, lineHeight: 21, color: "#555", textAlign: "right" },
  error: { color: "#b00020", padding: 16, textAlign: "center" },
  empty: { textAlign: "center", color: "#666", marginTop: 30 }
});
