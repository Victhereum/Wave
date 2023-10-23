 import React from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { addDurations } from '../../hooks/useCreateSrtFile';
import Colors from '../../theme/colors';

const SubtitleEditor = ({ subtitle, onSubtitleChange, index }: { subtitle: { Word: string, Duration: string, Offset: string }, onSubtitleChange: (text:string) => void, index :number}) => {
  const timeStamp = addDurations(subtitle.Duration, subtitle.Offset)
  

  return (
    <View style={styles.container}>
      <View>
      <Text style={styles.subtitleText}>{timeStamp}</Text>
      </View>
      <TextInput
        style={styles.subtitleInput}
        value={subtitle.Word}
        onChangeText={onSubtitleChange}
      />
    
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 10,
    // width: 300,
    marginRight:3
  },
  subtitleText: {
    fontSize: 16,
    marginBottom: 5,
    fontWeight: 'bold',
    color:Colors.primary
  },
  subtitleInput: {
    borderWidth: 0.2,
    borderColor: Colors.primary,
    borderRadius:3,
    padding: 7,
    textAlign:"center",
    color:"white",
    // width:300,
    marginBottom: 10,
  }
});

export default SubtitleEditor;
