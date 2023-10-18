import { createMaterialBottomTabNavigator } from "@react-navigation/material-bottom-tabs";
import Entypo from "react-native-vector-icons/Entypo";
import React from "react"; // Don't forget to import React

import { View, Text } from "react-native"; // Replace Image with Text
import Colors from "../theme/colors";
import Projects from "../screens/Home/Projects";
import Home from "../screens/Home/Home";
import Profile from "../screens/profile/Profile";

const Tab = createMaterialBottomTabNavigator();

function BottomTab() {
    return (
        <Tab.Navigator
            activeColor={Colors.primary}
            inactiveColor={Colors.black}
            barStyle={{ backgroundColor: Colors.black }}
        >
            <Tab.Screen
                name="Projects"
                component={Projects}
                options={{
                    headerShown: false,
                    tabBarLabel: "Home",
                    tabBarIcon: ({ color }: any) => (
                        <Entypo name="home" color={color} size={20} />
                    ),
                } as never}
            />
            <Tab.Screen
                name="Create"
                component={Home} // You may need to replace this with your create component
                options={({ navigation }) => ({ // Use options to customize the tab button
                    headerShown: false,
                    tabBarLabel: "Create",
                    tabBarButton: () => (
                        <View style={{ flex: 1, justifyContent: "center", alignItems: "center",backgroundColor:Colors.primary }}>
                            <Text style={{ color: Colors.white, fontSize: 16 }}>Create</Text>
                        </View>
                    ),
                })}
            />
            <Tab.Screen
                name="Profile"
                component={Profile}
                options={{
                    headerShown: false,
                    tabBarLabel: "Home",
                    tabBarIcon: ({ color }: any) => (
                        <Entypo name="home" color={color} size={20} />
                    ),
                } as never}
            />
        </Tab.Navigator>
    );
}

export default BottomTab;
