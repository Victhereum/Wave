import React, { useState, useEffect } from "react";
import {
  MD3LightTheme as DefaultTheme,
  Provider as PaperProvider,
} from "react-native-paper";
import FlashMessage from "react-native-flash-message";
import { NavigationContainer } from "@react-navigation/native";
import useAuthenticationState from "./states/zustandStore/authentication";
import AuthStack from "./routes/auth";
import MainStack from "./routes/application";

export default function App() {
  const isAuthenticated = useAuthenticationState((state) => state.authentication.isAuthenticated);

  const [islogged, setIslogged] = useState(false)


  useEffect(() => {
    if (isAuthenticated) {
      setIslogged(true)
    } else {
      setIslogged(false)
    }
  }, [isAuthenticated])

  const theme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      secondaryContainer: "none",
    },
  };

  return (
    <NavigationContainer>
      <PaperProvider theme={theme}>

        {
          !islogged ?
            <AuthStack />
            :
            <MainStack />
        }
      </PaperProvider>
      <FlashMessage position="bottom" />
    </NavigationContainer>
  );
}





