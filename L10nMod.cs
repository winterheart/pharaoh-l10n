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
using System.Security.Cryptography;
using System.Net;
using System.Runtime.Serialization;
using System.Linq;
using System.Runtime.CompilerServices;
using System;

namespace Pharaoh_L10n
{
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
            foreach (var code in codes)
            {
                if (code.opcode == OpCodes.Ldftn && (code.operand as MethodInfo).Name == "<OnEnable>b__79_0")
                {
                    MelonLogger.Msg($"Found opcode: {code.opcode.Name} : {(code.operand as MethodInfo).Name}");
                    code.operand = AccessTools.Method(typeof(Utils), "IsNotNote");
                }
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
