/*
This file is part of Pharaoh L10n project
SPDX-License-Identifier: GPL-3.0-or-later
(c) 2023 Azamat H. Hackimov <azamat.hackimov@gmail.com>
*/

using System.Collections.Generic;
using System.IO;
using System.Reflection;
using MelonLoader;
using UnityEngine;
using I2.Loc;
using HarmonyLib;
using System.Reflection.Emit;
using System.Linq;

namespace Pharaoh_L10n
{
    public static class Globals
    {
        // Version. First 3 digit - base version of game. 4th digit - version of mod.
        public const string fullver = "1.2.0.1";
        public const string semver = "1.2.0+p1";
    }
 
    public class L10nMod : MelonMod
    {
        private AssetBundle m_AssetBundle;

        public L10nMod()
        {
            using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream("Pharaoh_L10n.pharaoh-l10n.assetbundle"))
            using (var tempStream = new MemoryStream((int)stream.Length))
            {
                stream.CopyTo(tempStream);
                m_AssetBundle = AssetBundle.LoadFromMemory(tempStream.ToArray(), 0);
            }
        }

        public override void OnInitializeMelon()
        {
            LoggerInstance.Msg("Pharaoh l10n started");
            UpdateLocalization();
            PatchHarmony();
        }

        private void UpdateLocalization()
        {
            LocalizationManager.UpdateSources();
            // var csv = LocalizationManager.Sources[0].Export_CSV(string.Empty, ';');
            // File.WriteAllText("out.csv", csv);
            var translation_csv = m_AssetBundle.LoadAsset<TextAsset>("translation");
            LocalizationManager.Sources[0].Import_CSV(string.Empty, translation_csv.text, eSpreadsheetUpdateMode.Replace, ';');
            // Set language code. Just in case.
            LocalizationManager.Sources[0].mLanguages[5].Code = "ru";
            LocalizationManager.LocalizeAll(true);
            LoggerInstance.Msg("Updated translation");
        }

        private void PatchHarmony()
        {
            HarmonyInstance.PatchAll(typeof(OptionManager));
            LoggerInstance.Msg("Harmony patched");
        }
    }

    [HarmonyPatch(typeof(OptionManager))]
    [HarmonyPatch("OnEnable")]
    public static class OptionManager_OnEnable_Patch
    {
        static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
        {
            var codes = new List<CodeInstruction>(instructions);
            bool found = false;
            foreach (var code in codes.Select((name, index) => (name, index)))
            {
                if (code.name.opcode == OpCodes.Newobj &&
                    (code.name.operand as ConstructorInfo).FullDescription() == "void System.Func<string, bool>::.ctor(object object, IntPtr method)" &&
                    codes[code.index - 1].opcode == OpCodes.Ldftn
                    )
                {
                    MelonLogger.Msg($"Found anchor opcode");
                    MelonLogger.Msg($"Previous opcode: {codes[code.index - 1].opcode.Name} : {(codes[code.index - 1].operand as MethodInfo).Name}");
                    codes[code.index - 1].operand = AccessTools.Method(typeof(Utils), "IsNotNote");
                    found = true;
                }
               
            }
            if (!found)
            {
                MelonLogger.Warning($"Anchor opcode not found!");
            }
            return codes;
        }
    }

    public class Utils
    {
        public static bool IsNotNote(string l)
        {
            return (l != "(Note)");
        }
    }
}
