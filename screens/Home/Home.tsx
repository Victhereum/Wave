import React, { useRef } from "react";
import { Text, TouchableOpacity, View, Platform, ScrollView, useWindowDimensions } from "react-native";
import { styles as style } from "../../css/stylesheet";
import { StyleSheet, Button, ActivityIndicator } from 'react-native';
import { FFmpegKit, FFmpegKitConfig, ReturnCode } from 'ffmpeg-kit-react-native';
import { makeDirectoryAsync, getInfoAsync, cacheDirectory } from 'expo-file-system';
import { launchImageLibraryAsync, MediaTypeOptions } from 'expo-image-picker';
import { Video, AVPlaybackStatus } from 'expo-av';
import videoApiSdk from "../../services/video/video.service";
import useCreateSrtFile from "../../hooks/useCreateSrtFile";
import Empty from "../../components/home/Empty";
import CustomHeader from "../../components/common/customHeader";
import Colors from "../../theme/colors";
import Feather from 'react-native-vector-icons/Feather';
import AntDesign from 'react-native-vector-icons/AntDesign';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';

import RBSheet from "react-native-raw-bottom-sheet";
import ActionCard from "../../components/home/ActionCard";



const Home = ({ navigation }: any) => {
 

  const refRBSheet = useRef<any>();
  const { width } = useWindowDimensions()
  
  const handleNextPage = (pageName:string) => {
    navigation.navigate(pageName)
    refRBSheet.current.close()
  }

  return (
    <ScrollView style={{ flex: 1, height: '100%', backgroundColor: "#000000" }} contentContainerStyle={[{ margin: 0, backgroundColor: "#000000" }]}>
      <CustomHeader title="Projects" titleStyle={{ fontWeight: '600', fontSize: 20 }} rightIcon={<View style={{ backgroundColor: Colors.primary, height: 30, width: 30, borderRadius: 100, flexDirection: "column", alignItems: "center", justifyContent: 'center' }}><Feather name="plus" size={20} color="#fff" style={{ marginTop: 2 }} /></View>} onRightPress={() => refRBSheet.current.open()} />
      <View style={{
        height: "100%",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#000000"
      }}>

        <RBSheet
          ref={refRBSheet}
          closeOnDragDown={true}
          closeOnPressMask={false}
          height={400}
          customStyles={{
            wrapper: {
              backgroundColor: "transparent"
            },
            container: {
              backgroundColor: "rgba(29, 35, 41, 1)",
            },
            draggableIcon: {
              backgroundColor: "#000"
            }
          }}
        >
          <ScrollView>
            <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "center",width,paddingHorizontal:20,flexWrap:"wrap"}}>
              <View style={{ width: "46%" }}>
                <ActionCard icon={<AntDesign name="clouduploado" size={26} color={Colors.primary} style={{ marginBottom: 5 }} />} title={"Import"} subtext={"Upload your footage"} onPress={() => handleNextPage("converter")} />
              </View>
              <View style={{ width: "46%" }}>
                <ActionCard icon={<MaterialIcons name="online-prediction" size={26} color={Colors.primary} style={{ marginBottom: 5 }} />} title={"AI Dubbing"} subtext={"Translate your voice"} onPress={undefined} />
              </View>
            
            </View>
          </ScrollView>
        </RBSheet>
        <Empty onPress={()=>{}} />
      </View>
    </ScrollView>

  );
};

export default Home;



const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  videoContainer: {
    backgroundColor: '#ecf0f1',
    marginTop: 20,
    textAlign: 'center',
    padding: 10,

  },
  video: {
    alignSelf: 'center',
    width: 320,
    height: 200,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },

  headTitle: { color: "#CFD8D8", fontSize: 28, marginBottom: 20 },

  contentContainer: {
    flex: 1,
    alignItems: 'center',
  },
});

