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
            var translation_csv = m_AssetBundle.LoadAsset<TextAsset>("translation");
            // Remove garbage
            // LocalizationManager.Sources[0].mLanguages.RemoveRange(9, 7);
            LocalizationManager.Sources[0].Import_CSV(string.Empty, translation_csv.text, eSpreadsheetUpdateMode.Replace, ';');
            // Need to manually define code
            // LocalizationManager.Sources[0].mLanguages[9].Code = "ru";
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
            var innerTypes = typeof(OptionManager).GetNestedTypes(AccessTools.all); //; //.GetNestedTypes(AccessTools.all).Where(innerType => innerType.IsDefined(typeof(CompilerGeneratedAttribute)));
            foreach (var inner in innerTypes)
            {
                foreach (var method in inner.GetFields())
                {
                    MelonLogger.Msg($"Found inner: {inner} : {method}");
                }
            }

            //                .Where(innerType => innerType.IsDefined(typeof(CompilerGeneratedAttribute)));
            var codes = new List<CodeInstruction>(instructions);
            // var info = AccessTools.Field(typeof(OptionManager), "m_languageSelector");

            foreach (var code in codes)
            {
                //MelonLogger.Msg($"Found opcode: {code.opcode.Name} : {code.operand}");
            }

            //var startIndex = codes.FindIndex(ins => ins.opcode == OpCodes.Ldfld && ins.operand.Equals(info));
            //codes[startIndex + 2].opcode = OpCodes.Ldc_I4_S;
            //codes[startIndex + 2].operand = 9;

            // ins.opcode == OpCodes.Ldstr &&
            //var startIndex = codes.FindIndex(ins => ins.operand.Equals("Russian"));
            // {codes[startIndex].opcode.Name}
            //MelonLogger.Msg($"Found opcode: {codes[startIndex].operand}");
            //codes[startIndex].operand = "(Note)";
            IEnumerable<string> collection = LocalizationManager.GetAllLanguages().Where<string>((Func<string, bool>)(l => l != "(Note)")).Select<string, string>((Func<string, string>)(l => "Menu/Language/#" + l));
            return codes;
        }
    }
}
