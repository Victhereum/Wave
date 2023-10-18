import React, { useState } from "react";
import { Text, TouchableOpacity, View, Platform, ScrollView } from "react-native";
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



const getResultPath = async () => {
  const videoDir = `${cacheDirectory}video/`;

  // Checks if gif directory exists. If not, creates it
  async function ensureDirExists() {
    const dirInfo = await getInfoAsync(videoDir);
    if (!dirInfo.exists) {
      console.log("tmp directory doesn't exist, creating...");
      await makeDirectoryAsync(videoDir, { intermediates: true });
    }
  }

  await ensureDirExists();

  return `${videoDir}file2.mp4`;
}

const getSourceVideo = async () => {
  console.log('select video')
  const result = await launchImageLibraryAsync({
    mediaTypes: MediaTypeOptions.Videos
  })

  return (result.canceled) ? null : result.assets[0].uri
}


const Home = ({ navigation }: any) => {
  const [result, setResult] = React.useState('');
  const [source, setSource] = React.useState('');
  const [isLoading, setLoading] = React.useState(false);

  React.useEffect(() => {
    FFmpegKitConfig.init();
  }, []);

  const onPress = async () => {
    setLoading(() => true);
    setResult(() => '');

    const resultVideo = await getResultPath();
    const sourceVideo = await getSourceVideo();

    if (!sourceVideo) {
      setLoading(() => false);
      return;
    }
    setSource(() => sourceVideo)
    setLoading(() => false);

    // const ffmpegSession = await FFmpegKit
    //   .execute(`-i ${sourceVideo} -c:v mpeg4 -y ${resultVideo}`);

    // const result = await ffmpegSession.getReturnCode();

    // if (ReturnCode.isSuccess(result)) {
    //   setLoading(() => false);
    //   setResult(() => resultVideo);
    // } else {
    //   setLoading(() => false);
    //   console.error(result);
    // }

    translateVideo({ uri: sourceVideo })
    // console.log(sourceVideo)
  }


  const translateVideo = async ({ uri }: { uri: string }) => {
    console.log(uri)
    try {
      let formdata = new FormData();
      let uriArray = uri.split(".");
      let fileType = uriArray[uriArray.length - 1];

      const videoFilename = `${new Date()}.${fileType}`

      formdata.append('media', {
        name: videoFilename,
        type: 'video/*',
        uri: Platform.OS === 'ios' ? uri.replace('file://', '') : uri,
      } as any);

      const response = await videoApiSdk.getVideoAudioTranslationTranscription({ uri: formdata })
      // console.log("translateVideo success", response.data.captions)
      const ed = videoFilename.replace('.mp4', ' ')

      const getsrt = useCreateSrtFile(response?.data?.captions, ed)
      console.log(getsrt)

    } catch (error: any) {
      console.log("translateVideo failure", error?.response?.data || error)
    }
  }

  return (
    <ScrollView style={{ flex: 1, height: '100%', backgroundColor: "#000000" }} contentContainerStyle={[{ margin: 0, backgroundColor: "#000000" }]}>
      <CustomHeader title="Projects" titleStyle={{fontWeight:'600',fontSize:20}} rightIcon={<View style={{backgroundColor:Colors.primary,height:30,width:30,borderRadius:100,flexDirection:"column",alignItems:"center",justifyContent:'center'}}><Feather name="plus" size={20} color="#fff" style={{marginTop:2}}/></View>} onRightPress={onPress}/>
      <View style={{
        height: "100%",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#000000"
      }}>

        {
          !source && <Empty onPress={onPress} />
        }

        {isLoading && <ActivityIndicator size="large" color="#ff0033" />}
        {
          source &&
          <Plyr uri={source} title={'Source'} />
        }
        {result &&
          <Plyr uri={result} title={'Result'} />
        }
      </View>
    </ScrollView>

  );
};

export default Home;


const Plyr = (props: {
  title: string,
  uri: string,
}) => {
  const video = React.useRef(null);
  const [status, setStatus] = React.useState<AVPlaybackStatus | {}>({});

  return (
    <View style={styles.videoContainer}>
      <Text>{props.title}</Text>
      <Video
        ref={video}
        style={styles.video}
        source={{
          uri: props.uri,
        }}
        useNativeControls
        resizeMode="contain"
        isLooping
        onPlaybackStatusUpdate={(status: AVPlaybackStatus) => setStatus(() => status)}
      />
      <View style={styles.buttons}>
        <Button
          title={status?.isPlaying ? 'Pause' : 'Play'}
          disabled={(props.uri == '')}
          onPress={() =>
            status.isPlaying ? video?.current.pauseAsync() : video?.current.playAsync()
          }
        />
      </View>
    </View>
  );
}


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

  headTitle: { color: "#CFD8D8", fontSize: 28, marginBottom: 20 }
});

