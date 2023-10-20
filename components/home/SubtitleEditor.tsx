 import React from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

const SubtitleEditor = ({ subtitle, onSubtitleChange, onSaveSubtitle }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.subtitleText}>{subtitle.text}</Text>
      <TextInput
        style={styles.subtitleInput}
        value={subtitle.text}
        onChangeText={onSubtitleChange}
      />
      <Button
        title="Save"
        onPress={onSaveSubtitle}
        style={styles.saveButton}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 10,
    width:"100%"
  },
  subtitleText: {
    fontSize: 16,
    marginBottom: 5,
    color:'red'
  },
  subtitleInput: {
    borderWidth: 0.2,
    borderColor: '#ccc',
    borderRadius:10,
    padding: 5,
    color:"white",
    width:"100%",
    marginBottom: 10,
  },
  saveButton: {
    backgroundColor: 'blue',
    color: 'white',
  },
});

export default SubtitleEditor;
