import { useState } from "react";

interface ChatInputProps {
  onSubmit: (query: string) => void;
  disabled?: boolean;
}

export function ChatInput({onSubmit, disabled}: ChatInputProps){
  const [value, setValue] = useState("");

  function handleSubmit(e: React.SubmitEvent<HTMLFormElement>){
    e.preventDefault();
    const trimmed = value.trim();
    if(!trimmed || disabled) return;
    onSubmit(trimmed);
  }
  
  return (
    <form onSubmit={handleSubmit} className="chat-input">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="What would you like to research?"
        disabled={disabled}
      />
      <button type="submit" disabled={disabled || !value.trim()}>
        {disabled ? "Researching..." : "Ask"}
      </button>
    </form>
  );
}
