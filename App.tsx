import React,{useState,useEffect} from "react";
import Routes from "./routes/route";
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

  return (
    <NavigationContainer>
      {
        !islogged ?
          <AuthStack />
          :
          <MainStack />
      }

      <FlashMessage position="bottom" />
    </NavigationContainer>
  );
}





