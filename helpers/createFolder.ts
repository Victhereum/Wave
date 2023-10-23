import { cacheDirectory, makeDirectoryAsync, writeAsStringAsync, documentDirectory } from 'expo-file-system';
const createFolder = async (folderName?: string) => {
    try {
        // Create the directory if it doesn't exist.
        const srtFolderPath = `${documentDirectory}/${folderName ?? "wave"}`;
        await makeDirectoryAsync(srtFolderPath, { intermediates: true });
        console.log('folder created successfully at:', srtFolderPath);
        return srtFolderPath;
    } catch (error) {
        console.error('Error creating folder:', error);
        return false
    }
}

export default createFolder;