import * as React from "react";
import Routes from "./routes/route";
import { NavigationProvider } from "./context/NavigationContext";
import FlashMessage from "react-native-flash-message";

export default function App() {
 
  return (
    <NavigationProvider>
      <Routes />
      <FlashMessage position="bottom" />
    </NavigationProvider>
  );
}





