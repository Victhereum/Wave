import React from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  StyleSheet,
  Text,
  View,
  ImageBackground,
  StatusBar,
  Image,
  TouchableOpacity,
} from "react-native";
import * as NavigationBar from "expo-navigation-bar";
import { styles } from "../css/stylesheet";

export default function Payment({ navigation }) {
  useFocusEffect(
    React.useCallback(() => {
      // This code will run when the screen is in focus
      NavigationBar.setBackgroundColorAsync("#472B6F");

      return () => {
        NavigationBar.setBackgroundColorAsync("#000000");
      };
    }, [])
  );

  return (
    <View style={styless.container}>
      <ImageBackground
        source={require("../assets/paymentbg.png")}
        resizeMode="cover"
        style={styless.image}
      >
        <StatusBar
          barStyle="light-content"
          backgroundColor="transparent"
          translucent={true}
        />
        <View
          style={{
            alignItems: "center",
            justifyContent: "center",
            marginTop: 200,
          }}
        >
          <Text style={styless.text}>Advanced</Text>
          <Text style={[styless.text, { fontSize: 40 }]}>Video Editor</Text>
          <View style={{ display: "flex", flexDirection: "row", gap: 20 }}>
            <View
              style={{
                width: 60,
                display: "flex",
                flexDirection: "column",
                gap: 10,
                alignItems: "center",
                justifyContent: "center",
                marginVertical: 20,
              }}
            >
              <View
                style={{
                  backgroundColor: styles.secondaryColor,
                  borderRadius: 50,
                  padding: 10,
                }}
              >
                <Image
                  source={require("../assets/benefit1.png")}
                  resizeMode="contain"
                  style={{ width: 30, height: 30 }}
                />
              </View>
              <Text
                style={{
                  color: "white",
                  textTransform: "capitalize",
                  textAlign: "center",
                }}
              >
                Premium filters
              </Text>
            </View>
            <View
              style={{
                width: 60,
                display: "flex",
                flexDirection: "column",
                gap: 10,
                alignItems: "center",
                justifyContent: "center",
                marginVertical: 20,
              }}
            >
              <View
                style={{
                  backgroundColor: "white",
                  borderRadius: 50,
                  padding: 10,
                }}
              >
                <Image
                  source={require("../assets/benefit2.png")}
                  resizeMode="contain"
                  style={{ width: 30, height: 30 }}
                />
              </View>
              <Text
                style={{
                  color: "white",
                  textTransform: "capitalize",
                  textAlign: "center",
                }}
              >
                Unlimited editing
              </Text>
            </View>
            <View
              style={{
                width: 60,
                display: "flex",
                flexDirection: "column",
                gap: 10,
                alignItems: "center",
                justifyContent: "center",
                marginVertical: 20,
              }}
            >
              <View
                style={{
                  backgroundColor: styles.secondaryColor,
                  borderRadius: 50,
                  padding: 10,
                }}
              >
                <Image
                  source={require("../assets/benefit3.png")}
                  resizeMode="contain"
                  style={{ width: 30, height: 30 }}
                />
              </View>
              <Text
                style={{
                  color: "white",
                  textTransform: "capitalize",
                  textAlign: "center",
                }}
              >
                no ads & watermark
              </Text>
            </View>
          </View>
          <View style={{ marginVertical: 10 }}>
            <Text
              style={{
                color: "white",
                textTransform: "capitalize",
                textAlign: "center",
                fontSize: 16,
              }}
            >
              7 days free trial.
            </Text>
            <Text
              style={{
                color: "white",
                textTransform: "capitalize",
                textAlign: "center",
                fontSize: 16,
              }}
            >
              after trial $5.66/month
            </Text>
          </View>
          <TouchableOpacity
            style={{ ...styles.primaryButton, width: "90%", marginTop: 20 }}
            onPress={() => navigation.navigate("Subscription")}
          >
            <Text style={styles.mediumText}>Subscribe</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={{
              ...styles.primaryButton,
              width: "90%",
              marginTop: 20,
              backgroundColor: "white",
            }}
            onPress={() => navigation.navigate("Home")}
          >
            <Text style={[styles.mediumText, { color: styles.primaryColor }]}>
              Free trial
            </Text>
          </TouchableOpacity>
        </View>
      </ImageBackground>
    </View>
  );
}

const styless = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#472B6FFF",
  },
  image: {
    flex: 1,
    justifyContent: "center",
  },
  text: {
    color: "white",
    fontSize: 24,
    lineHeight: 48,
    fontWeight: "bold",
    textAlign: "center",
    // backgroundColor: "#000000c0",
    width: "100%",
  },
});
