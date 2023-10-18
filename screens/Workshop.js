import React, { useState, useEffect } from "react";
import { Text, View, TouchableOpacity, Image, TextInput } from "react-native";
import { Video, ResizeMode } from "expo-av";
import { styles } from "../css/stylesheet";
import { useFocusEffect } from "@react-navigation/native";
import { VideoService } from "../services/VideoService";
import { FFmpegKit } from "ffmpeg-kit-react-native";
import {
  VESDK,
  VideoEditorModal,
  Configuration,
} from "react-native-videoeditorsdk";

const Workshop = ({ navigation, route }) => {
  const [image, setImage] = useState(null);
  const video = React.useRef(null);
  const [status, setStatus] = useState({});
  const [actionToggle, setActionToggle] = useState({
    selected: false,
    name: "",
  });

  const actions = [
    { name: "Trim", icon: require("../assets/trim.png") },
    { name: "Audio", icon: require("../assets/audio.png") },
    { name: "Caption", icon: require("../assets/subtitles.png") },
    { name: "Save", icon: require("../assets/save.png") },
    { name: "Delete", icon: require("../assets/delete.png") },
  ];

  const { setFromLanguages, setToLanguages } =

  useFocusEffect(
    React.useCallback(() => {
      // This code will run anytime the screen is in focus
      setImage(route.params.image);
      return () => setImage(null);
    }, [])
  );

  // This code will run only the very first time the screen is in focus
  useEffect(() => {
    const fetchLang = async () => {
      const data = await VideoService.getLanguages();
      setFromLanguages(data.data.from_languages);
      setToLanguages(data.data.to_languages);
    };
    fetchLang();

    return () => {
      fetchLang();
    };
  }, []);

  const handleActionPress = async (actionName, index) => {
    // console.log(image);
    // FFmpegKit.execute(
    //   `ffmpeg -i ${image?.assets[0]?.uri} -c:v copy -c:a copy output.mkv`
    // ).then(async (session) => {
    //   // const returnCode = await session.getReturnCode();
    //   const log = session.getLogsAsString();
    //   console.log(log);
    //   // if (ReturnCode.isSuccess(returnCode)) {
    //   //   // SUCCESS
    //   // } else if (ReturnCode.isCancel(returnCode)) {
    //   //   // CANCEL
    //   // } else {
    //   //   // ERROR
    //   // }
    // });

    VESDK.openEditor(require("./testvid.mp4"));

    // const session = await FFmpegKit.execute(
    //   `ffmpeg -i ${image?.assets[0]?.uri} -c:v copy -c:a copy output.mkv`
    // );
    // console.log(session);

    setActionToggle((prev) => {
      return { ...prev, selected: true, name: actionName };
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.smallText}>Video.mp4</Text>
      <View
        style={{
          width: "100%",
          height: "auto",
          backgroundColor: "black",
          borderWidth: 1,
          borderRadius: 10,
          borderColor: styles.secondaryColor,
        }}
      >
        <Video
          ref={video}
          style={{ width: "100%", height: 300 }}
          source={{
            uri: image?.assets[0]?.uri,
          }}
          useNativeControls
          resizeMode={ResizeMode.CONTAIN}
          isLooping
          onPlaybackStatusUpdate={(status) => setStatus(() => status)}
        />
        {/* <View style={styles.primaryButton}>
          <Button
            title={status.isPlaying ? "Pause" : "Play"}
            onPress={() =>
              status.isPlaying
                ? video.current.pauseAsync()
                : video.current.playAsync()
            }
          />
        </View> */}
      </View>
      {/* <VideoEditorModal visible={true} video={require("./testvid.mp4")} /> */}
      <View
        style={{
          marginTop: 20,
          width: "100%",
          padding: 10,
          borderRadius: 10,
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "space-between",
          borderWidth: 1,
          borderRadius: 10,
          borderColor: styles.secondaryColor,
        }}
      >
        {actions.map((action, index) => (
          <View
            key={index}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: 5,
            }}
          >
            <TouchableOpacity
              key={index}
              style={{
                backgroundColor: `${
                  actionToggle.name === actions.name
                    ? styles.secondaryColor
                    : "#f1f1f1"
                }`,
                borderRadius: 50,
                padding: 10,
              }}
              onPress={() => handleActionPress(action.name, index)}
            >
              <Image
                source={action.icon}
                resizeMode="contain"
                style={{ width: 20, height: 20 }}
              />
            </TouchableOpacity>
            <Text style={styles.smallText}>{action.name}</Text>
          </View>
        ))}
      </View>
      {actionToggle.selected === true ? (
        <View
          style={{
            width: "100%",
            height: 200,
            borderWidth: 1,
            borderTopColor: styles.secondaryColor,
            borderLeftColor: styles.secondaryColor,
            borderRightColor: styles.secondaryColor,
            position: "absolute",
            bottom: 0,
            borderTopLeftRadius: 10,
            borderTopRightRadius: 10,
          }}
        >
          <Text style={[styles.smallText, { textAlign: "center" }]}>
            {actionToggle.name}
          </Text>
          <Text>What language is spoken in the video?</Text>
          <TextInput placeholder="french" />
        </View>
      ) : (
        ""
      )}
    </View>
  );
};

export default Workshop;
