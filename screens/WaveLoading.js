import React, { useEffect } from "react";
import { View, Animated, StyleSheet, Easing, Text } from "react-native";
import { styles } from "../css/stylesheet";

const WaveLoader = () => {
  const lineAnimations = [...Array(6)].map(() => new Animated.Value(0));
  const duration = 1000;

  const animateLines = () => {
    const animations = lineAnimations.map((lineAnim, index) => {
      return Animated.sequence([
        Animated.timing(lineAnim, {
          toValue: 100,
          duration: (duration / 3) * index,
          useNativeDriver: false,
          easing: Easing.linear,
        }),
        Animated.timing(lineAnim, {
          toValue: 25,
          duration: duration,
          useNativeDriver: false,
          easing: Easing.linear,
        }),
      ]);
    });

    Animated.loop(Animated.stagger(10, animations)).start();
  };

  useEffect(() => {
    animateLines();
    return () => {
      // Clean up animations when unmounting
      lineAnimations.forEach((lineAnim) => {
        lineAnim.removeAllListeners();
      });
    };
  }, []);

  return (
    <View style={styles.waveLoaderContainer}>
      <View
        style={{
          display: "flex",
          height: "10%",
          width: "100%",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "row",
          gap: 10,
        }}
      >
        {lineAnimations.map((lineAnim, index) => (
          <Animated.View
            key={index}
            style={[
              styles.waveLoaderLine,
              {
                height: lineAnim.interpolate({
                  inputRange: [0, 100],
                  outputRange: ["0%", "100%"],
                }),
              },
            ]}
          />
        ))}
      </View>
      <View>
        <Text style={styles.bigText}>Loading</Text>
      </View>
    </View>
  );
};

export default WaveLoader;
