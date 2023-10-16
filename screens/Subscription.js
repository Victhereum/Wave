import React, { useState } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  StyleSheet,
  Text,
  View,
  ImageBackground,
  StatusBar,
  Image,
  TouchableOpacity,
  TextInput,
  Animated,
  ActivityIndicator,
} from "react-native";
import * as NavigationBar from "expo-navigation-bar";
import { styles } from "../css/stylesheet";

export default function Subscription({ navigation }) {
  const [fullName, setFullName] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCVV] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [activeButtonIndex, setActiveButtonIndex] = useState(0);
  const [cardPayment, setCardPayment] = useState(true);
  const [googlePay, setGooglePay] = useState(false);
  const [applePay, setApplePay] = useState(false);

  const buttons = [
    {
      label: "card payment",
      icon: require("../assets/credit-card.png"),
    },
    { label: "google pay", icon: require("../assets/google-pay.png") },
    { label: "apple pay", icon: require("../assets/apple-pay.png") },
  ];

  const lineAnimations = buttons.map(() => new Animated.Value(0));

  const animateLine = (index) => {
    setActiveButtonIndex((prevState) => {
      prevState + index;
    });

    expandLine(index);
  };

  const expandLine = (index) => {
    Animated.timing(lineAnimations[index], {
      toValue: 1,
      duration: 500,
      useNativeDriver: false,
    }).start();

    lineAnimations.forEach((lineAnim, i) => {
      if (i !== index) {
        Animated.timing(lineAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: false,
        }).start();
      }
    });

    if (index === 0) {
      setCardPayment(true);
      setGooglePay(false);
      setApplePay(false);
    }
    if (index === 1) {
      setCardPayment(false);
      setGooglePay(true);
      setApplePay(false);
    }
    if (index === 2) {
      setGooglePay(false);
      setCardPayment(false);
      setApplePay(true);
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      NavigationBar.setBackgroundColorAsync("#472B6F");
      expandLine(activeButtonIndex);

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
        <View style={styles.paymentShadow}>
          <Text style={styless.text}>Choose payment method</Text>
          <View style={styles.paymentTypes}>
            {buttons.map((item, index) => {
              return (
                <View style={styles.paymentTypeContainer} key={index}>
                  <TouchableOpacity
                    style={styles.paymentTypeContainer.icon}
                    onPress={() => animateLine(index)}
                  >
                    <Image
                      source={item?.icon}
                      resizeMode="contain"
                      style={{ width: 40, height: 40 }}
                    />
                  </TouchableOpacity>
                  <Text style={styles.paymentTypeContainer.text}>
                    {item?.label}
                  </Text>
                  <Animated.View
                    style={{
                      width: "100%",
                      height: 2,
                      backgroundColor: "#9457EB",

                      transform: [{ scaleX: lineAnimations[index] }],
                    }}
                  ></Animated.View>
                </View>
              );
            })}
          </View>
          {cardPayment && (
            <>
              <TextInput
                placeholder="Card Name, e.g: John Doe"
                onChangeText={(text) => setFullName(text)}
                value={fullName}
                style={styles.input}
                placeholderTextColor={"gray"}
              />
              <TextInput
                inputMode="numeric"
                placeholder="Card Number, e.g: XXXX-XXXX-XXXX-XXXX"
                onChangeText={(text) => setCardNumber(text)}
                value={cardNumber}
                style={styles.input}
                placeholderTextColor={"gray"}
              />
              <View style={{ display: "flex", flexDirection: "row" }}>
                <TextInput
                  inputMode="numeric"
                  placeholder="Expiry Date, e.g: 01/1991"
                  onChangeText={(text) => setExpiry(text)}
                  value={expiry}
                  style={styles.cardExpiry}
                  placeholderTextColor={"gray"}
                />
                <TextInput
                  secureTextEntry={true}
                  maxLength={3}
                  inputMode="numeric"
                  placeholder="CVV"
                  onChangeText={(text) => setCVV(text)}
                  value={cvv}
                  style={styles.cardCVV}
                  placeholderTextColor={"gray"}
                />
              </View>
              <Text style={{ color: "white", marginTop: 5 }}>
                You will be billed $5.66 monthly
              </Text>
              <TouchableOpacity
                style={{ ...styles.primaryButton, width: "90%", marginTop: 20 }}
                onPress={() => navigation.navigate("WaveLoader")}
              >
                <Text style={styles.mediumText}>Pay</Text>
              </TouchableOpacity>
            </>
          )}
          {googlePay && (
            <View
              style={{
                height: 300,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <ActivityIndicator />
            </View>
          )}
          {applePay && (
            <View
              style={{
                height: 300,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <ActivityIndicator />
            </View>
          )}
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
    backgroundColor: "#000000c0",
  },
  text: {
    color: "white",
    fontSize: 24,
    lineHeight: 100,
    fontWeight: "bold",
    textAlign: "center",
    // backgroundColor: "#000000c0",
    width: "100%",
  },
});
