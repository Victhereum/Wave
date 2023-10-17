import { useEffect } from 'react';
import { cacheDirectory, makeDirectoryAsync, writeAsStringAsync } from 'expo-file-system';

interface Ifile {
    Offset: string;
    Duration: string;
    Word: string;
}

const useCreateSrtFile = async (srtData: Ifile[], videoFilename: string) => {
    const srtContent = srtData
        .map((item, index) => {
            const endTime = addDurations(item?.Duration, item?.Offset);
            const entry = [
                (index + 1).toString(),
                `${item.Offset} --> ${endTime}`,
                item.Word,
            ];
            return entry.join('\n');
        })
        .join('\n\n');
    
    let filepath =""

    try {
        // Create the directory if it doesn't exist.
        const srtFolderPath = `${cacheDirectory}${videoFilename}`;
        await makeDirectoryAsync(srtFolderPath, { intermediates: true });

        // Define the SRT file path.
        const srtFilePath = `${srtFolderPath}/${videoFilename}.srt`.replace(/ /g, ''); // Remove spaces in the filename.

        filepath = srtFilePath
        // Write the SRT content to the file.
        await writeAsStringAsync(srtFilePath, srtContent);

        console.log('SRT file saved successfully at:', srtFilePath);
    } catch (error) {
        console.error('Error writing or creating SRT file:', error);
    }

    return {
        srtContent,
        path: filepath,
    };
};

function addDurations(duration1: string, offset: string): string {
    const [hours1, minutes1, seconds1, milliseconds1] = duration1.split(/:|\./).map(Number);
    const [hours2, minutes2, seconds2, milliseconds2] = offset.split(/:|\./).map(Number);

    const totalMilliseconds = (hours1 + hours2) * 3600000 + (minutes1 + minutes2) * 60000 + (seconds1 + seconds2) * 1000 + (milliseconds1 + milliseconds2);

    const hours = Math.floor(totalMilliseconds / 3600000);
    const minutes = Math.floor((totalMilliseconds % 3600000) / 60000);
    const seconds = Math.floor((totalMilliseconds % 60000) / 1000);
    const milliseconds = totalMilliseconds % 1000;

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(milliseconds).padStart(3, '0')}`;
}

export default useCreateSrtFile;
export { Ifile };
export { addDurations };



