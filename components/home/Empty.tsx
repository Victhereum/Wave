import React, { useState } from "react";
import { Text, TouchableOpacity, View, useWindowDimensions } from "react-native";
import { styles as style } from "../../css/stylesheet";
import { StyleSheet } from 'react-native';
import AntDesign from 'react-native-vector-icons/AntDesign';
import Colors from "../../theme/colors";


const Empty = ({ onPress }: { onPress: () => void }) => {
    const { height } = useWindowDimensions()
    return (
        <View style={{ width: "53%", height: height/ 1.3, flexDirection: 'column', justifyContent: "center", alignItems: "center" }}>
            <AntDesign name="folderopen" color={Colors.grey} size={100} />
            <Text style={[styles.headTitle, { fontWeight: "700" }]}>No Projects yet</Text>
            <Text
                style={[style.smallText, { textAlign: "center", marginBottom: 20, fontSize: 14, lineHeight: 23, fontWeight: "600" }]}
            >
                To upload your first projects and witness some magic, click the button
                below.
            </Text>
            {/* <TouchableOpacity style={style.primaryButton} onPress={onPress}>
                <Text style={style.mediumText}>Create</Text>
            </TouchableOpacity> */}
        </View>
    )
}

export default Empty

const styles = StyleSheet.create({
    headTitle: { color: "#CFD8D8", fontSize: 28, marginBottom: 20 }

})