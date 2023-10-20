import { StyleSheet, Text, View, TouchableOpacity } from 'react-native'
import React from 'react'
import Colors from '../../theme/colors'

const ActionCard = ({ icon, title, subtext, onPress }: { icon: any, title: string, subtext: string, onPress: any }) => {
    return (
        <TouchableOpacity style={{ flexDirection: 'column', alignItems: 'center',justifyContent:"center", marginTop: 10, backgroundColor:"rgba(255, 255, 255, 0.1)", width: "100%", padding: 10, borderRadius: 10,height:100 }} onPress={onPress}>
            {icon}
            <View style={{alignItems:"center",justifyContent:"center"}}>
                <Text style={{ fontSize: 16, fontWeight: '500', color: Colors.white }}>{title}</Text>
                <Text style={{ fontSize: 12, color: '#666',marginTop:4 }}>{subtext}</Text>
            </View>
        </TouchableOpacity>
    )
}

export default ActionCard

const styles = StyleSheet.create({})