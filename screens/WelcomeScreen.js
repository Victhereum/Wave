import React from "react";
import {
  View,
  Text,
  ScrollView,
  SafeAreaView,
  Image,
  TouchableOpacity,
} from "react-native";
import { StatusBar } from "expo-status-bar";

import { styles } from "../css/stylesheet";
import { useRoute } from "@react-navigation/native";
// import CustomModal from "../components/Modal";

function WelcomeScreen({ navigation, route }) {

  const [modalVisible, setModalVisible] = React.useState(false);

  const showModal = () => {
    setModalVisible(true);
  };

  const hideModal = () => {
    setModalVisible(false);
  };

  const routename = useRoute();


  React.useEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <TouchableOpacity onPress={showModal} style={styles.hamburger}>
          <Text style={styles.hamburger.text}>≡</Text>
        </TouchableOpacity>
      ),
    });
  }, [navigation]);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.container}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.container}>
          {/* <CustomModal visible={modalVisible} onClose={hideModal} /> */}
          <Image
            style={{ width: 300, height: 300 }}
            resizeMode="contain"
            source={require("../assets/icon.png")}
          />
          <TouchableOpacity
            style={{ ...styles.primaryButton, marginTop: 20 }}
            onPress={() => navigation.navigate("RegisterDevice")}
          >
            <Text style={styles.mediumText}>Add Device</Text>
          </TouchableOpacity>
          <StatusBar style="light" backgroundColor="#262626" />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

export default WelcomeScreen;
