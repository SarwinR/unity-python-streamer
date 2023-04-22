using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;


public class CameraStreamer : MonoBehaviour
{
    Thread thread;

    public int width, height;

    public string host = "127.0.0.1";
    public int port = 1234;

    private RenderTexture renderTexture;
    private Socket socket;
    private bool connected = false;

    
    Queue<byte[]> buffer = new Queue<byte[]>();
    

    void Start()
    {
        renderTexture = new RenderTexture(width, height, 24, RenderTextureFormat.ARGB32);
        GetComponent<Camera>().targetTexture = renderTexture;

        thread = new Thread(SendFrame);
        thread.Start();
    }

    private void Update()
    {
        RenderTexture.active = renderTexture;
        Texture2D texture = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.ARGB32, false);
        texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
        texture.Apply();

        byte[] data = texture.GetRawTextureData();
        buffer.Clear();
        buffer.Enqueue(data);
    }

    void SendFrame(object data)
    {
        while (true)
        {
            if (connected)
            {
                if(buffer.TryDequeue(out byte[] bufferData))
                {
                    try
                    {
                        socket.Send(bufferData);
                    }
                    catch
                    {
                        connected = false;
                        print("Lost connection!");
                    }
                }
            }
            else
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
                }
            }
        }
    }

    void OnApplicationQuit()
    {
        if (connected)
        {
            socket.Close();
        }
        thread.Abort();
    }
}