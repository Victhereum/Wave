import { createMaterialBottomTabNavigator } from "@react-navigation/material-bottom-tabs";
import Entypo from "react-native-vector-icons/Entypo";
import AntDesign from "react-native-vector-icons/AntDesign";
import FontAwesome from "react-native-vector-icons/FontAwesome";
import React from "react"; // Don't forget to import React

import { View, Text, Button } from "react-native"; // Replace Image with Text
import Colors from "../theme/colors";
import Projects from "../screens/Home/Projects";
import Home from "../screens/Home/Home";
import Profile from "../screens/profile/Profile";

const Tab = createMaterialBottomTabNavigator();

function BottomTab() {
    return (
        <Tab.Navigator
            activeColor={Colors.white}
            inactiveColor={Colors.grey}
            barStyle={{ backgroundColor: Colors.black }}
        >
            {/* <Tab.Screen
                name="Projects"
                component={Projects}
                options={{
                    headerShown: false,
                    tabBarLabel: "Projects",
                    tabBarIcon: ({ color }: any) => (
                        <AntDesign name="inbox" color={color} size={20} />
                    ),
                } as never}
            /> */}
            <Tab.Screen
                name="Create"
                component={Home} // You may need to replace this with your create component
                options={({ navigation }) => ({ // Use options to customize the tab button
                    headerShown: false,
                    tabBarLabel: "Create",
                    tabBarIcon: ({ color }: any) => (
                        <AntDesign name="inbox" color={color} size={20} />
                    ),
                })}
            />
            <Tab.Screen
                name="Profile"
                component={Profile}
                options={{
                    headerShown: false,
                    tabBarLabel: "Profile",
                    tabBarIcon: ({ color }: any) => (
                        <FontAwesome name="user-o" color={color} size={20} />
                    ),
                } as never}
            />
        </Tab.Navigator>
    );
}

export default BottomTab;
