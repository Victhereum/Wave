import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  StyleSheet,
} from "react-native";
import { useRoute, useFocusEffect } from "@react-navigation/native";
import SelectDropdown from "react-native-select-dropdown";
import { StatusBar } from "expo-status-bar";
import FontAwesome from "react-native-vector-icons/FontAwesome";
import Ionicons from "react-native-vector-icons/Ionicons";
import { NavigationContext } from "../context/NavigationContext";
import { AuthService } from "../services/AuthService";
import { styles } from "../css/stylesheet";

function AuthScreen({ navigation }) {
  const [isSignIn, setIsSignIn] = useState(false);
  const [countriess, setCountries] = useState([{}]);
  const [secureTextEntry, setSecureTextEntry] = useState(true);
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const { setCurrentScreen } = React.useContext(NavigationContext);

  const route = useRoute();
  const currentScreenName = route.name;

  const victor = [
    {
      code: "+93",
      flag: "https://flagcdn.com/w320/af.png",
      name: "Afghanistan",
      iso: "AF",
    },
    {
      code: "+358",
      flag: "https://flagcdn.com/w320/ax.png",
      name: "Åland Islands",
      iso: "AX",
    },
    {
      code: "+355",
      flag: "https://flagcdn.com/w320/al.png",
      name: "Albania",
      iso: "AL",
    },
    {
      code: "+213",
      flag: "https://flagcdn.com/w320/dz.png",
      name: "Algeria",
      iso: "DZ",
    },
    {
      code: "+1-684",
      flag: "https://flagcdn.com/w320/as.png",
      name: "American Samoa",
      iso: "AS",
    },
    {
      code: "+376",
      flag: "https://flagcdn.com/w320/ad.png",
      name: "Andorra",
      iso: "AD",
    },
    {
      code: "+244",
      flag: "https://flagcdn.com/w320/ao.png",
      name: "Angola",
      iso: "AO",
    },
    {
      code: "+1-264",
      flag: "https://flagcdn.com/w320/ai.png",
      name: "Anguilla",
      iso: "AI",
    },
    {
      code: "+1-268",
      flag: "https://flagcdn.com/w320/ag.png",
      name: "Antarctica",
      iso: "AQ",
    },
    {
      code: "+54",
      flag: "https://flagcdn.com/w320/ar.png",
      name: "Antigua and Barbuda",
      iso: "AG",
    },
    {
      code: "+374",
      flag: "https://flagcdn.com/w320/am.png",
      name: "Argentina",
      iso: "AR",
    },
    {
      code: "+297",
      flag: "https://flagcdn.com/w320/aw.png",
      name: "Armenia",
      iso: "AM",
    },
    {
      code: "+61",
      flag: "https://flagcdn.com/w320/au.png",
      name: "Aruba",
      iso: "AW",
    },
    {
      code: "+43",
      flag: "https://flagcdn.com/w320/at.png",
      name: "Australia",
      iso: "AU",
    },
    {
      code: "+994",
      flag: "https://flagcdn.com/w320/az.png",
      name: "Austria",
      iso: "AT",
    },
    {
      code: "+1-242",
      flag: "https://flagcdn.com/w320/bs.png",
      name: "Bahamas",
      iso: "BS",
    },
    {
      code: "+880",
      flag: "https://flagcdn.com/w320/bd.png",
      name: "Bahrain",
      iso: "BH",
    },
    {
      code: "+1-246",
      flag: "https://flagcdn.com/w320/bb.png",
      name: "Bangladesh",
      iso: "BD",
    },
    {
      code: "+375",
      flag: "https://flagcdn.com/w320/by.png",
      name: "Barbados",
      iso: "BB",
    },
    {
      code: "+32",
      flag: "https://flagcdn.com/w320/be.png",
      name: "Belarus",
      iso: "BY",
    },
    {
      code: "+501",
      flag: "https://flagcdn.com/w320/bz.png",
      name: "Belgium",
      iso: "BE",
    },
    {
      code: "+229",
      flag: "https://flagcdn.com/w320/bj.png",
      name: "Belize",
      iso: "BZ",
    },
    {
      code: "+1-441",
      flag: "https://flagcdn.com/w320/bm.png",
      name: "Benin",
      iso: "BJ",
    },
    {
      code: "+975",
      flag: "https://flagcdn.com/w320/bt.png",
      name: "Bermuda",
      iso: "BM",
    },
  ];

  const countriesWithFlags = [
    { title: "Egypt", image: require("./Images/Egypt.png"), code: "+122" },
    { title: "Canada", image: require("./Images/Canada.png"), code: "+232" },
    {
      title: "Australia",
      image: require("./Images/Australia.png"),
      code: "+555",
    },
    { title: "Ireland", image: require("./Images/Ireland.png"), code: "+71" },
  ];

  useFocusEffect(
    React.useCallback(() => {
      // This code will run when the screen is in focus
      setCurrentScreen(currentScreenName);
      const fetchData = async () => {
        await AuthService.getCountries();
      };
      // fetchData();
    }, [])
  );

  const toggleSignIn = () => {
    // Toggle between sign-in and sign-up forms
    setIsSignIn(!isSignIn);
  };

  const handleSignIn = () => {
    // toggleSignIn();
    navigation.navigate("Payment");
  };

  const handleSignUp = async () => {
    toggleSignIn();
  };

  const handleForgotPassword = () => {
    // navigate to forgot password here.
    navigation.navigate("ForgotPassword");
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" backgroundColor="#000000" />
      <Text style={styles.headerText}>Wave</Text>
      <Text
        style={[
          styles.smallText,
          {
            marginBottom: 40,
            textAlign: "center",
            width: "80%",
            color: "gray",
          },
        ]}
      >
        Transform Your Videos with our Editing Magic, make the best captions
      </Text>

      {/* Conditional Rendering Based on isSignIn */}
      {!isSignIn && (
        <>
          <Text
            style={{ ...styles.smallText, textAlign: "left", width: "90%" }}
          >
            Full Name
          </Text>
          <TextInput
            placeholder="John Doe"
            onChangeText={(text) => setFullName(text)}
            value={fullName}
            style={styles.input}
            placeholderTextColor={"gray"}
          />
          <Text
            style={{ ...styles.smallText, textAlign: "left", width: "90%" }}
          >
            Phone Number
          </Text>
          <View style={{ display: "flex", flexDirection: "row", gap: 0 }}>
            <View style={styles.countryDropDown}>
              <SelectDropdown
                data={victor}
                onSelect={(selectedItem, index) => {
                  console.log(selectedItem, index);
                }}
                buttonStyle={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
                  justifyContent: "space-between",
                  backgroundColor: "#000",
                  width: "100%",
                  height: 30,
                  padding: 0,
                  margin: 0,
                }}
                renderCustomizedButtonChild={(selectedItem, index) => {
                  return (
                    <View
                      key={index}
                      style={{
                        display: "flex",
                        flexDirection: "row",
                        width: "100%",
                        alignItems: "center",
                        justifyContent: "space-between",
                      }}
                    >
                      {selectedItem ? (
                        <Image
                          source={{
                            uri: selectedItem.flag,
                            cache: "only-if-cached",
                            method: "GET",
                          }}
                          style={styless.dropdown3BtnImage}
                        />
                      ) : (
                        <Ionicons
                          name="md-earth-sharp"
                          color={"#777"}
                          size={15}
                        />
                      )}
                      <Text style={{ color: "white" }}>
                        {selectedItem ? selectedItem.code : ""}
                      </Text>
                      <FontAwesome
                        name="chevron-down"
                        color={"#777"}
                        size={15}
                      />
                    </View>
                  );
                }}
                dropdownStyle={styless.dropdown3DropdownStyle}
                rowStyle={styless.dropdown3RowStyle}
                selectedRowStyle={styless.dropdown1SelectedRowStyle}
                renderCustomizedRowChild={(item, index) => {
                  return (
                    <View style={styless.dropdown3RowChildStyle}>
                      <Image
                        source={item.image}
                        style={styless.dropdownRowImage}
                      />
                    </View>
                  );
                }}
              />
            </View>
            <TextInput
              keyboardType="numeric"
              placeholder="Phone number"
              onChangeText={(text) => setPhone(text)}
              value={phone}
              style={styles.phoneInput}
              placeholderTextColor={"gray"}
            />
          </View>
          <TouchableOpacity
            style={{
              ...styles.primaryButton,
              width: "90%",
              marginVertical: 20,
            }}
            onPress={handleSignUp}
          >
            <Text style={styles.mediumText}>Sign Up</Text>
          </TouchableOpacity>
          <Text style={styles.smallText}>Already have an account?</Text>
          <TouchableOpacity
            style={{
              ...styles.primaryButton,
              backgroundColor: "black",
              borderWidth: 1,
              width: "40%",
              borderColor: styles.secondaryColor,
              marginTop: 20,
            }}
            onPress={() => setIsSignIn(true)}
          >
            <Text style={styles.mediumText}>Sign In</Text>
          </TouchableOpacity>
        </>
      )}

      {isSignIn && (
        <>
          {/* <Text
            style={{ ...styles.smallText, textAlign: "left", width: "90%" }}
          >
            Select your country
          </Text> */}
          <Text
            style={{ ...styles.smallText, textAlign: "left", width: "90%" }}
          >
            Phone Number
          </Text>
          <View style={{ display: "flex", flexDirection: "row", gap: 0 }}>
            <View style={styles.countryDropDown}>
              <SelectDropdown
                data={victor}
                onSelect={(selectedItem, index) => {
                  console.log(selectedItem, index);
                }}
                buttonStyle={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
                  justifyContent: "space-between",
                  backgroundColor: "#000",
                  width: "100%",
                  height: 30,
                  padding: 0,
                  margin: 0,
                }}
                renderCustomizedButtonChild={(selectedItem, index) => {
                  return (
                    <View
                      key={index}
                      style={{
                        display: "flex",
                        flexDirection: "row",
                        width: "100%",
                        alignItems: "center",
                        justifyContent: "space-between",
                      }}
                    >
                      {selectedItem ? (
                        <Image
                          source={{
                            uri: selectedItem.flag,
                            cache: "only-if-cached",
                            method: "GET",
                          }}
                          style={styless.dropdown3BtnImage}
                        />
                      ) : (
                        <Ionicons
                          name="md-earth-sharp"
                          color={"#777"}
                          size={15}
                        />
                      )}
                      <Text style={{ color: "white" }}>
                        {selectedItem ? selectedItem.code : ""}
                      </Text>
                      <FontAwesome
                        name="chevron-down"
                        color={"#777"}
                        size={15}
                      />
                    </View>
                  );
                }}
                dropdownStyle={styless.dropdown3DropdownStyle}
                rowStyle={styless.dropdown3RowStyle}
                selectedRowStyle={styless.dropdown1SelectedRowStyle}
                renderCustomizedRowChild={(item, index) => {
                  return (
                    <View style={styless.dropdown3RowChildStyle}>
                      <Image
                        source={item.image}
                        style={styless.dropdownRowImage}
                      />
                    </View>
                  );
                }}
              />
            </View>
            <TextInput
              keyboardType="numeric"
              placeholder="Phone number"
              onChangeText={(text) => setPhone(text)}
              value={phone}
              style={styles.phoneInput}
              placeholderTextColor={"gray"}
            />
          </View>
          <Text
            style={{ ...styles.smallText, textAlign: "left", width: "90%" }}
          >
            One-Time-Password
          </Text>
          <View style={{ display: "flex", flexDirection: "row", gap: 0 }}>
            <TextInput
              placeholder="Enter the OTP you recieved"
              onChangeText={(text) => setPassword(text)}
              value={password}
              keyboardType="numeric"
              maxLength={6}
              style={styles.passwordInput}
              placeholderTextColor={"gray"}
            />
            <TouchableOpacity
              // onPress={() => setSecureTextEntry(!secureTextEntry)}
              style={styles.passwordToggle}
            >
              <Text style={styles.smallText}>Get OTP</Text>
            </TouchableOpacity>
          </View>
          <TouchableOpacity
            style={{
              ...styles.primaryButton,
              width: "90%",
              marginVertical: 20,
            }}
            onPress={handleSignIn}
          >
            <Text style={styles.mediumText}>Sign In</Text>
          </TouchableOpacity>
          <Text style={styles.smallText}>Don't have an account?</Text>
          <TouchableOpacity
            style={{
              ...styles.primaryButton,
              backgroundColor: "black",
              borderWidth: 1,
              width: "40%",
              borderColor: styles.secondaryColor,
              marginTop: 20,
            }}
            onPress={() => setIsSignIn(false)}
          >
            <Text style={styles.mediumText}>Sign Up</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
}

export default AuthScreen;

const styless = StyleSheet.create({
  shadow: {
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 10,
  },
  header: {
    flexDirection: "row",
    // width,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#F6F6F6",
  },
  headerTitle: { color: "#000", fontWeight: "bold", fontSize: 16 },
  saveAreaViewContainer: { flex: 1, backgroundColor: "#FFF" },
  viewContainer: {
    flex: 1,
    // width,
    backgroundColor: "#FFF",
  },
  scrollViewContainer: {
    flexGrow: 1,
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: "10%",
    paddingBottom: "20%",
  },

  dropdown1BtnStyle: {
    width: "80%",
    height: 50,
    backgroundColor: "#FFF",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#444",
  },
  dropdown1BtnTxtStyle: { color: "#444", textAlign: "left" },
  dropdown1DropdownStyle: { backgroundColor: "#EFEFEF" },
  dropdown1RowStyle: {
    backgroundColor: "#EFEFEF",
    borderBottomColor: "#C5C5C5",
  },
  dropdown1RowTxtStyle: { color: "#444", textAlign: "left" },
  dropdown1SelectedRowStyle: { backgroundColor: "rgba(0,0,0,0.1)" },
  dropdown1searchInputStyleStyle: {
    backgroundColor: "#EFEFEF",
    borderRadius: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#444",
  },

  dropdown2BtnStyle: {
    width: "80%",
    height: 50,
    backgroundColor: "#444",
    borderRadius: 8,
  },
  dropdown2BtnTxtStyle: {
    color: "#FFF",
    textAlign: "center",
    fontWeight: "bold",
  },
  dropdown2DropdownStyle: {
    backgroundColor: "#444",
    borderRadius: 12,
  },
  dropdown2RowStyle: { backgroundColor: "#444", borderBottomColor: "#C5C5C5" },
  dropdown2RowTxtStyle: {
    color: "#FFF",
    textAlign: "center",
    fontWeight: "bold",
  },
  dropdown2SelectedRowStyle: { backgroundColor: "rgba(255,255,255,0.2)" },
  dropdown2searchInputStyleStyle: {
    backgroundColor: "#444",
    borderBottomWidth: 1,
    borderBottomColor: "#FFF",
  },

  dropdown3BtnStyle: {
    width: "80%",
    height: 50,
    backgroundColor: "#FFF",
    paddingHorizontal: 0,
    borderWidth: 1,
    borderRadius: 8,
    borderColor: "#444",
  },
  dropdown3BtnChildStyle: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 18,
  },
  dropdown3BtnImage: { width: 15, height: 15, resizeMode: "contain" },
  dropdown3BtnTxt: {
    color: "#444",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 24,
    marginHorizontal: 12,
  },
  dropdown3DropdownStyle: { backgroundColor: "slategray" },
  dropdown3RowStyle: {
    backgroundColor: "slategray",
    borderBottomColor: "#444",
    height: 50,
  },
  dropdown3RowChildStyle: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "flex-start",
    alignItems: "center",
    paddingHorizontal: 18,
  },
  dropdownRowImage: { width: 15, height: 15, resizeMode: "cover" },
  dropdown3RowTxt: {
    color: "#F1F1F1",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 24,
    marginHorizontal: 12,
  },
  dropdown3searchInputStyleStyle: {
    backgroundColor: "slategray",
    borderBottomWidth: 1,
    borderBottomColor: "#FFF",
  },
});
