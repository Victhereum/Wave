import React, { useEffect, useRef } from "react";
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
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Ionicons from 'react-native-vector-icons/Ionicons';
import SubtitleEditor from "../../components/home/SubtitleEditor";

const getSourceVideo = async () => {
    console.log('select video')
    const result = await launchImageLibraryAsync({
        mediaTypes: MediaTypeOptions.Videos
    })

    return (result.canceled) ? null : result.assets[0].uri
}

const Converter = ({navigation}:any) => {
    const [subtitles, setsubtitles] = React.useState([]);
    const [source, setSource] = React.useState('');
    const [isLoading, setLoading] = React.useState(false);

    React.useEffect(() => {
        FFmpegKitConfig.init();
    }, []);

    const onPress = async () => {
        setLoading(() => true);

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
    }


    useEffect(() => {
        onPress()
    }, [])


    let uriArray = source.split(".");
    let fileType = uriArray[uriArray.length - 1];
    const videoFilename = `${new Date()}.${fileType}`
    const videoFilenameed = videoFilename.replace('.mp4', ' ')


    const translateVideo = async ({ uri }: { uri: string }) => {
        try {
            let formdata = new FormData();
            formdata.append('media', {
                name: videoFilename,
                type: 'video/*',
                uri: Platform.OS === 'ios' ? uri.replace('file://', '') : uri,
            } as any);

            const response = await videoApiSdk.getVideoAudioTranslationTranscription({ uri: formdata })

            setsubtitles(response?.data?.captions)
            console.log(response?.data?.captions)
        } catch (error: any) {
            console.log("translateVideo failure", error?.response?.data || error)
        }
    }

    const handleCompile = () => {
        const getsrt = useCreateSrtFile(subtitles, videoFilenameed)
        console.log(getsrt)
    }

    return (
        <ScrollView style={{ flex: 1, height: '100%', backgroundColor: "#000000" }} contentContainerStyle={[{ margin: 0, backgroundColor: "#000000" }]}>
            <CustomHeader title=" " titleStyle={{ fontWeight: '600', fontSize: 20 }} rightIcon={<View style={{ backgroundColor: Colors.primary, height: 30, width: 30, borderRadius: 100, flexDirection: "column", alignItems: "center", justifyContent: 'center' }}><MaterialCommunityIcons name="database-export" size={20} color="#fff" style={{ marginTop: 2 }} /></View>} onRightPress={handleCompile} leftIcon={<View style={{ height: 30, width: 30, borderRadius: 100, flexDirection: "column", alignItems: "center", justifyContent: 'center' }}><Ionicons name="arrow-back" size={20} color="#fff" style={{ marginTop: 2 }} /></View>} onLeftPress={()=> navigation.goBack()} />
            <View style={{
                height: "100%",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "#000000"
            }}>

                {isLoading && <ActivityIndicator size="large" color="#ff0033" />}
                {
                    source &&
                    <>
                    <Plyr uri={source} />
                    {
                        subtitles.length > 0 && subtitles.map((item)=>
                        <SubtitleEditor subtitle={item?.Word} onSubtitleChange={()=>{}} onSaveSubtitle={()=>{}} />
                        )
                    }
                    </>
                }

            </View>
        </ScrollView>
    );
}

export default Converter


const Plyr = (props: {
    uri: string
}) => {
    const video = React.useRef(null);
    const [status, setStatus] = React.useState<AVPlaybackStatus | {}>({});

    return (
            <Video
                ref={video}
                style={styles.video}
                source={{
                    uri: props.uri,
                }}
                useNativeControls
                resizeMode="contain"
                onPlaybackStatusUpdate={(status: AVPlaybackStatus) => setStatus(() => status)}
            />
            // <View style={styles.buttons}>
            //     <Button
            //         title={status?.isPlaying ? 'Pause' : 'Play'}
            //         disabled={(props.uri == '')}
            //         onPress={() =>
            //             status.isPlaying ? video?.current.pauseAsync() : video?.current.playAsync()
            //         }
            //     />
            // </View>
    );
}



const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    video: {
        alignSelf: 'center',
        width: "100%",
        height:300,
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
