import React, { useState } from "react";
import { Text, TouchableOpacity, View, StatusBar } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import * as ImagePicker from "expo-image-picker";
import { styles } from "../css/stylesheet";
import { NavigationContext } from "../context/NavigationContext";

const Home = ({ navigation }) => {
  const [image, setImage] = useState(null);

  const pickFile = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
      selectionLimit: 1,
    });

    console.log(result);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
      navigation.navigate("Workshop", { image: result });
    }
  };

  const { fromLanguages, toLanguages } = React.useContext(NavigationContext);

  useFocusEffect(
    React.useCallback(() => {
      // This code will run anytime the screen is in focus
      console.log(fromLanguages, "use focus effect - from lang");
      console.log(toLanguages, "use focus effect - to lang");
    }, [])
  );

  return (
    <View style={styles.container}>
      <View
        style={{
          position: "absolute",
          top: StatusBar.currentHeight + 10,
          left: 20,
        }}
      >
        <Text style={styles.smallText}>My Activities</Text>
      </View>
      <View style={{ width: "90%", alignItems: "center" }}>
        <Text style={styles.headerText}>No Projects</Text>
        <Text
          style={[styles.mediumText, { textAlign: "center", marginBottom: 20 }]}
        >
          To upload your first projects and witness some magic, click the button
          below.
        </Text>
        <TouchableOpacity style={styles.primaryButton} onPress={pickFile}>
          <Text style={styles.mediumText}>Create</Text>
        </TouchableOpacity>
      </View>
      {/* {image && (
        <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />
      )} */}
    </View>
  );
};

export default Home;
