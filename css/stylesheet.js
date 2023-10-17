import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  primaryColor: "#000000",
  secondaryColor: "#9457EB",
  red: "#D20202",

  white: "#F1C93B",

  headerText: { color: "#9457EB", fontSize: 28, marginBottom: 20 },

  bigText: { color: "#CFD8D8", fontSize: 24 },

  mediumText: { color: "#CFD8D8", fontSize: 20 },

  smallText: { color: "#CFD8D8", fontSize: 16 },

  waveLoaderContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "column",
    backgroundColor: "black",
    gap: 20,
  },

  waveLoaderLine: {
    width: 10,
    backgroundColor: "#9457EB",
    borderRadius: 50,
  },

  cardExpiry: {
    width: "60%",
    padding: 10,
    marginVertical: 10,
    borderRightWidth: 1,
    borderLeftWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderLeftColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderRightColor: "#9457EB",
    borderBottomLeftRadius: 50,
    borderTopLeftRadius: 50,
    color: "#ffffff",
  },

  cardCVV: {
    width: "30%",
    padding: 10,
    marginVertical: 10,
    borderRightWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderRightColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderTopRightRadius: 50,
    borderBottomRightRadius: 50,
    color: "#ffffff",
  },

  header: {
    headerStyle: {
      backgroundColor: "#262626",
    },
    headerTintColor: "#CFD8D8",
    headerTitleStyle: {
      fontWeight: "bold",
    },
  },

  greeting: {
    color: "#CFD8D8",
    fontSize: 12,
    textTransform: "capitalize",
    person: {
      color: "#CFD8D8",
      fontSize: 16,
      fontWeight: "bold",
      textTransform: "capitalize",
    },
  },

  hamburger: {
    backgroundColor: "#262626",
    width: 50,
    height: 50,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",

    text: {
      color: "#CFD8D8",
      fontSize: 32,
    },
  },

  splashHeaderText: { color: "#D20202", fontSize: 24, marginTop: 10 },

  splashHeaderSubText: {
    color: "#CFD8D8",
    fontSize: 16,
    textAlign: "center",
    marginVertical: 10,
  },

  scrollviewContainer: {
    flex: 1,
    width: "100%",
    // alignItems: "center",
    // justifyContent: "center",
    backgroundColor: "#262626",
  },

  container: {
    flex: 1,
    margin: 0,
    height:"100%",
    alignItems: "center",
    // justifyContent: "center",
    backgroundColor: "#000000",
  },

  paymentShadow: {
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#000000c0",
    borderRadius: 50,
    paddingBottom: 50,
  },

  paymentTypes: {
    display: "flex",
    flexDirection: "row",
    gap: 30,
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
  },

  paymentTypeContainer: {
    width: 50,
    display: "flex",
    flexDirection: "column",
    gap: 10,
    alignItems: "center",
    justifyContent: "center",
    marginVertical: 20,
    icon: {
      backgroundColor: "white",
      padding: 10,
      borderRadius: 50,
    },
    text: {
      color: "white",
      textTransform: "capitalize",
      textAlign: "center",
    },
  },

  primaryButton: {
    backgroundColor: "#9457EB",
    width: 300,
    height: 50,
    borderRadius: 50,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
  },

  input: {
    width: "90%",
    padding: 10,
    margin: 10,
    fontSize: 16,
    borderColor: "#9457EB",
    borderWidth: 1,
    borderRadius: 50,
    color: "#ffffff",
  },

  phoneInput: {
    width: "67.5%",
    padding: 10,
    fontSize: 16,
    marginVertical: 10,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderLeftColor: "#9457EB",
    borderRightColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderTopRightRadius: 50,
    borderBottomRightRadius: 50,
    color: "#ffffff",
  },

  countryDropDown: {
    width: "22.5%",
    alignItems: "center",
    justifyContent: "center",
    padding: 10,
    marginVertical: 10,
    borderRightWidth: 0,
    borderLeftWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderLeftColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderBottomLeftRadius: 50,
    borderTopLeftRadius: 50,
    color: "#ffffff",
  },

  passwordInput: {
    width: "70%",
    padding: 10,
    fontSize: 16,
    marginVertical: 10,
    borderRightWidth: 0,
    borderLeftWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderLeftColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderBottomLeftRadius: 50,
    borderTopLeftRadius: 50,
    color: "#ffffff",
  },

  passwordToggle: {
    width: "20%",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#9457EB",
    padding: 10,
    marginVertical: 10,
    borderRightWidth: 1,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderRightColor: "#9457EB",
    borderTopColor: "#9457EB",
    borderBottomColor: "#9457EB",
    borderTopRightRadius: 50,
    borderBottomRightRadius: 50,
  },

  forgotPasswordInputContainer: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 20,
    width: "100%",
    alignItems: "center",
  },

  forgotPasswordInput: {
    width: 50,
    height: 60,
    borderWidth: 1,
    borderColor: "gray",
    textAlign: "center",
    fontSize: 20,
    marginRight: 5,
    borderRadius: 10,
    color: "white",
  },
});
