"use client";

import { useEffect, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
  image?: string; // base64 or object URL
};

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content:
          "Hello! I'm Gaurav, your real estate assistant. How can I help you today?",
      },
    ]);
  }, []);

  const handleSend = async () => {
    if (!input && !file) return;
    const reader = new FileReader();
    if (file) {
      reader.onloadend = () => {
        const imageUrl = reader.result as string;
        setMessages((prev) => [
          ...prev,
          { role: "user", content: input, image: imageUrl },
        ]);
        // then send it to backend
      };
      reader.readAsDataURL(file);
    } else {
      setMessages((prev) => [...prev, { role: "user", content: input }]);
    }

    const formData = new FormData();
    formData.append("message", input);
    if (file) formData.append("image", file);
    formData.append("history", JSON.stringify(messages));

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.response },
    ]);

    setInput("");
    setFile(null);
  };

  return (
    <div className="flex flex-col max-w-2xl mx-auto min-h-screen bg-white border shadow-md p-4">
      <h2 className="text-xl font-bold mb-4 text-center">
        🏘️ Real Estate Assistant
      </h2>

      <div className="flex flex-col gap-2 overflow-y-auto h-[500px] px-2 py-3 border rounded bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-[75%] px-4 py-2 rounded-lg text-sm whitespace-pre-wrap ${
              msg.role === "user"
                ? "bg-blue-500 text-white self-end"
                : "bg-gray-200 text-gray-900 self-start"
            }`}
          >
            {msg.image && (
              <img
                src={msg.image}
                alt="uploaded"
                className="max-w-full rounded mb-2"
              />
            )}
            {msg.content}
          </div>
        ))}
      </div>

      <div className="flex items-center gap-2 mt-4">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="w-35 text-sm"
        />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message and/or describe the image..."
          className="flex-1 p-2 border rounded text-sm"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
