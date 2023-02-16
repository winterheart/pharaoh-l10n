#if UNITY_EDITOR
using UnityEditor;
using System.IO;

public class CreateAssetBundles
{
    [MenuItem("Assets/Build AssetBundles")]
    static void BuildAllAssetBundles()
    {
        string assetBundleDirectory = "Assets/AssetBundles";
        string assetName = "pharaoh-l10n.assetbundle";
        Directory.Delete(assetBundleDirectory, true);
        Directory.CreateDirectory(assetBundleDirectory);
        BuildPipeline.BuildAssetBundles(assetBundleDirectory,
                                        BuildAssetBundleOptions.ChunkBasedCompression,
                                        BuildTarget.StandaloneWindows);

        File.Copy(Path.Combine(assetBundleDirectory, assetName), Path.Combine("../..", assetName), true);
    }
}
#endif
