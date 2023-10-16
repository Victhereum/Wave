import React from "react";
import { showMessage } from "react-native-flash-message";
import { Button } from "react-native-paper";

const Alert = {
  success(message: string) {
    showMessage({
      message: message,
      type: "success",
      backgroundColor: "#589C5F",
      // titleStyle: { fontFamily: 'MabryPro' },
      duration: 5000,
      renderCustomContent: () => (
        <Button
          style={{
            marginTop: 20,
            borderRadius: 100,
            backgroundColor: "rgba(255,255,255,0.2)",
          }}
          labelStyle={{ color: "#fff" }}
          uppercase={false}
          mode="outlined"
        >
          Dismiss
        </Button>
      ),
    });
  },
  error(message: string) {
    showMessage({
      message: message,
      type: "danger",
      backgroundColor: "#FB3F4A",
      // titleStyle: { fontFamily: 'MabryPro' },
      duration: 5000,
      renderCustomContent: () => (
        <Button
          style={{
            marginTop: 20,
            borderRadius: 100,
            backgroundColor: "rgba(255,255,255,0.2)",
          }}
          labelStyle={{ color: "#fff" }}
          uppercase={false}
          mode="outlined"
        >
          Dismiss
        </Button>
      ),
    });
  }
}

export default Alert;