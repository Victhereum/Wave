import React, { useEffect, useRef } from "react";
import { Text, TouchableOpacity, View, Platform, ScrollView, useWindowDimensions } from "react-native";
import { styles as style } from "../../css/stylesheet";
import { StyleSheet, Button, ActivityIndicator } from 'react-native';
import { FFmpegKit, FFmpegKitConfig, ReturnCode } from 'ffmpeg-kit-react-native';
import { launchImageLibraryAsync, MediaTypeOptions } from 'expo-image-picker';
import { Video, AVPlaybackStatus } from 'expo-av';
import videoApiSdk from "../../services/video/video.service";
import useCreateSrtFile from "../../hooks/useCreateSrtFile";
import CustomHeader from "../../components/common/customHeader";
import Colors from "../../theme/colors";
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Ionicons from 'react-native-vector-icons/Ionicons';
import SubtitleEditor from "../../components/home/SubtitleEditor";
import createFolder from "../../helpers/createFolder";


const getSourceVideo = async () => {
    console.log('select video')
    const result = await launchImageLibraryAsync({
        mediaTypes: MediaTypeOptions.Videos
    })

    return (result.canceled) ? null : result.assets[0].uri
}

const Converter = ({ navigation }: any) => {
    const [subtitles, setsubtitles] = React.useState<{ Word: string, Duration: string, Offset: string }[]>([]);
    const [source, setSource] = React.useState('');

    // result gotten from adding translation
    const [result, setResult] = React.useState('');

    const [isLoading, setLoading] = React.useState(false);

    React.useEffect(() => {
        FFmpegKitConfig.init();
    }, []);

    const onPress = async () => {

        const sourceVideo = await getSourceVideo();

        if (!sourceVideo) {
            setLoading(() => false);
            return;
        }
        setSource(() => sourceVideo)

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
        setLoading(true)
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
            setLoading(false)

        } catch (error: any) {
            setLoading(false)
            console.log("translateVideo failure", error?.response?.data || error)
        }
    }


    const handleCompile = async () => {
        try {
            console.log("Compilation started...");

            // Generate the SRT file
            const getsrt = await useCreateSrtFile(subtitles, videoFilenameed);
            console.log("Generating SRT in progress...");

            // Create the video path
            const resultVideo = createFolder() + videoFilename;
            console.log("Creating video path...");

            if (resultVideo) {
                console.log("Loading video with SRT...");

                // Get the SRT file path
                const path = getsrt.path;

                // Construct the FFmpeg command
                const ffmpegCommand = `-i ${source} -vf "subtitles='${path}'" ${resultVideo}`;


                console.log({ ffmpegCommand });


                // Execute the FFmpeg command
                const ffmpegSession = await FFmpegKit.execute(ffmpegCommand);

                const output = await ffmpegSession.getOutput();
                console.log("FFmpeg Session Output:", output);


                if (ffmpegSession) {
                    const returnCode = await ffmpegSession.getReturnCode();

                    if (ReturnCode.isSuccess(returnCode)) {
                        console.log("Loading video with SRT successful...");
                        setLoading(false);
                        setResult(resultVideo);
                        console.log("Result stored here:", { resultVideo });
                    } else {
                        setLoading(false);
                        console.error("Error in FFmpeg command execution. ReturnCode:", returnCode);
                    }
                } else {
                    console.error("FFmpeg execution failed. ffmpegSession is null.");
                }
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    };


    const handleSubtitleEditing = (index: number, text: string) => {
        // Make a copy of the subtitles array to avoid mutating the state directly
        const updatedSubtitles = [...subtitles];
        updatedSubtitles[index].Word = text;
        setsubtitles(updatedSubtitles);

    }

    return (
        <ScrollView style={{ flex: 1, height: '100%', backgroundColor: "#000000" }} contentContainerStyle={[{ margin: 0, backgroundColor: "#000000" }]}>
            <CustomHeader title=" " titleStyle={{ fontWeight: '600', fontSize: 20 }} rightIcon={<View style={{ backgroundColor: Colors.primary, height: 30, width: 30, borderRadius: 100, flexDirection: "column", alignItems: "center", justifyContent: 'center' }}><MaterialCommunityIcons name="database-export" size={20} color="#fff" style={{ marginTop: 2 }} /></View>} onRightPress={handleCompile} leftIcon={<View style={{ height: 30, width: 30, borderRadius: 100, flexDirection: "column", alignItems: "center", justifyContent: 'center' }}><Ionicons name="arrow-back" size={20} color="#fff" style={{ marginTop: 2 }} /></View>} onLeftPress={() => navigation.goBack()} />
            <View style={{
                height: "100%",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "#000000"
            }}>

                {isLoading && <View>
                    <ActivityIndicator color={Colors.primary} size={22} />
                    <Text style={{ color: Colors.white, fontSize: 14 }}>Loading video and subtitle</Text>
                </View>}
                {
                    source &&
                    <>
                        <Plyr uri={source} />
                        <ScrollView style={styles.subtitleEditoContainer} horizontal>
                            {
                                subtitles.length > 0 && subtitles.map((item: { Word: string, Duration: string, Offset: string }, index) =>
                                    <SubtitleEditor subtitle={item} onSubtitleChange={(text: string) => handleSubtitleEditing(index, text)} index={index} />
                                )
                            }
                        </ScrollView>
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
        <View style={styles.videoContainer}>
            <Video
                ref={video}
                style={styles.video}
                source={{
                    uri: props.uri,
                }}
                useNativeControls
                resizeMode="cover"
                onPlaybackStatusUpdate={(status: AVPlaybackStatus) => setStatus(() => status)}
            />
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
    video: {
        alignSelf: 'center',
        width: "100%",
        height: 500,
    },
    videoContainer: {
        backgroundColor: '#ecf0f1',
        margin: 8,
        borderRadius: 8,
        justifyContent: 'center',
        alignItems: 'center',
        width: "100%",
    }
    ,
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

    subtitleEditoContainer: {
        backgroundColor: "rgba(29, 35, 41, 1)",
        padding: 3,
        borderRadius: 5
    }
});
