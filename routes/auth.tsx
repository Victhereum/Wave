import * as React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { TouchableOpacity, Text, View } from "react-native";
import AuthScreen from "../screens/AuthScreen";
import Payment from "../screens/Payment";
import Subscription from "../screens/Subscription";
import WaveLoader from "../screens/WaveLoading";
import Home from "../screens/Home/Home";
import Workshop from "../screens/Workshop";


const Stack = createNativeStackNavigator();

export default function AuthStack() {

    return (
        <Stack.Navigator initialRouteName="Auth" >
            <Stack.Screen
                options={{ headerShown: false }}
                name="Auth"
                component={AuthScreen}
            />
            <Stack.Screen
                options={{ headerShown: false }}
                name="Payment"
                component={Payment}
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
            <Stack.Screen
                options={{ headerShown: false }}
                name="Home"
                component={Home}
            />
            <Stack.Screen
                options={{ headerShown: false }}
                name="Workshop"
                component={Workshop}
            />
            {/* <Stack.Screen
                options={({ navigation, route }) => ({
                    headerTitle: () => (
                        <View>
                            <Text style={styles.greeting}>good morning,</Text>
                            <Text style={styles?.person}>{route.params?.name}</Text>
                        </View>
                    ),
                    headerRight: () => (
                        <TouchableOpacity style={styles.hamburger}>
                            <Text style={styles.hamburger.text}>≡</Text>
                        </TouchableOpacity>
                    ),
                })}
                name="Welcome"
                component={WelcomeScreen}
            /> */}
        </Stack.Navigator>
    );
}
