import * as React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { TouchableOpacity, Text, View } from "react-native";
import AuthScreen from "../screens/AuthScreen";
import WelcomeScreen from "../screens/WelcomeScreen";
import Payment from "../screens/Payment";
import Subscription from "../screens/Subscription";
import WaveLoader from "../screens/WaveLoading";
import Home from "../screens/Home/Home";
import Workshop from "../screens/Workshop";

import { styles } from "../css/stylesheet";
import { NavigationContext } from "../context/NavigationContext";
import BottomTab from "./bottomBarTab";

const Stack = createNativeStackNavigator();

export default function MainStack() {
    return (
        <Stack.Navigator initialRouteName="Payment" >
            <Stack.Screen
                options={{ headerShown: false }}
                name="Payment"
                component={Payment}
            />
            <Stack.Screen
                options={{ headerShown: false }}
                name="Home"
                component={BottomTab}
            />
            <Stack.Screen
                options={{ headerShown: false }}
                name="Subscription"
                component={Subscription}
            />
            <Stack.Screen
                options={{ headerShown: false }}
                name="WaveLoader"
                component={WaveLoader}
            />
           
        </Stack.Navigator>
    );
}
