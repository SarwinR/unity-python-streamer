using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;

public class CameraStreamer : MonoBehaviour
{
    public int width, height;

    public string host = "127.0.0.1";
    public int port = 1234;

    private RenderTexture renderTexture;
    private Socket socket;
    private bool connected;

    

    void Start()
    {
        // Initialize the texture
        renderTexture = new RenderTexture(720, 480, 24, RenderTextureFormat.ARGB32);
        Camera.main.targetTexture = renderTexture;

        // Start the connection process in a separate thread
        connected = false;

        InvokeRepeating("TryConnect", 0f, 1f);
    }

    void Update()
    {
        if (connected)
        {
            RenderTexture.active = renderTexture;
            Texture2D texture = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.ARGB32, false);
            texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
            texture.Apply();


            byte[] data = texture.GetRawTextureData();
            try
            {
                socket.Send(data);
            }
            catch
            {
                connected = false;
                print("Lost connection!");
            }
        }
    }


    void TryConnect()
    {
        if (!connected)
        {
            try
            {
                // Attempt to connect to the server
                socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                socket.Connect(host, port);

                // Connection successful
                connected = true;
                Debug.Log("Connected to " + host + ":" + port);
            }
            catch (SocketException e)
            {
                // Connection failed
                Debug.LogWarning("Failed to connect to " + host + ":" + port + " - " + e.Message);

                // Wait for a short time before trying again
                Thread.Sleep(1000);
            }
        }
    }

    void OnApplicationQuit()
    {
        if (connected)
        {
            // Close the socket if it's still open
            socket.Close();
        }
    }
}