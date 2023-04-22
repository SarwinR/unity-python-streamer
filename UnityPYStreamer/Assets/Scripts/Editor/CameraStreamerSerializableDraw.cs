using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

[CustomPropertyDrawer(typeof(CameraStreamer))]
public class CameraStreamerSerializableDraw : PropertyDrawer
{
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        EditorGUI.BeginProperty(position, label, property);

        SerializedProperty width = property.FindPropertyRelative("width");
        SerializedProperty height = property.FindPropertyRelative("height");

        Rect labelPosition = new Rect(position.x, position.y, position.width, position.height);
    
        position = EditorGUI.PrefixLabel(labelPosition, 
            EditorGUIUtility.GetControlID(FocusType.Passive),
            new GUIContent(width.objectReferenceValue!=null? "TEST": "Empty"));
    }
}
