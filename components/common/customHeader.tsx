import React from 'react'; // Import React
import { View, TouchableOpacity, StyleSheet, SafeAreaView, Text } from 'react-native';
import Colors from '../../theme/colors';

interface TCustomHeader {
    title?: string,
    leftIcon?: any,
    rightIcon?: any,
    onLeftPress?: () => void,
    onRightPress?: () => void,
    headerStyle?: any,
    titleStyle?: any
}

const CustomHeader = ({ title, leftIcon, rightIcon, onLeftPress, onRightPress, headerStyle, titleStyle }: TCustomHeader) => {
    return (
        <SafeAreaView> 
            <View style={[styles.headerContainer, headerStyle]}>
                <View style={{ width: "10%" }}>
                    {leftIcon && onLeftPress && (
                        <TouchableOpacity onPress={onLeftPress} style={styles.iconContainer}>
                            {leftIcon}
                        </TouchableOpacity>
                    )}
                </View>
                <View style={{ width: "80%", justifyContent: "center", alignItems: "center" }}>
                    <Text style={[styles.title, titleStyle]}>{title}</Text>
                </View>
                <View style={{ width: "10%" }}>
                    {rightIcon && onRightPress && (
                        <TouchableOpacity onPress={onRightPress} style={styles.iconContainer}>
                            {rightIcon}
                        </TouchableOpacity>
                    )}
                </View>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    headerContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 16,
        paddingVertical:5,
        height: 100,
    },
    iconContainer: {
        padding: 8,
    },
    title: {
        fontSize: 18,
        color: 'white',
    },
});

export default CustomHeader;
