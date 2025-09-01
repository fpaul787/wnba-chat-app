import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';


import { BehaviorSubject } from 'rxjs';

import { ChatService } from './chat.service';

// Message model
export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('wnba-chat');

  userMessage = '';
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  messages$ = this.messagesSubject.asObservable();

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    // Initialize user message or perform any setup logic here
  }

  sendMessage(){
    const query = this.userMessage.trim();
    if (!query) return;

    const current = this.messagesSubject.value;
    this.messagesSubject.next([...current, { role: 'user', content: query }]);
    this.userMessage = '';

    this.chatService.sendMessage(query).subscribe({
      next: (res) => {
        const updated = this.messagesSubject.value;
        this.messagesSubject.next([...updated, { role: 'assistant', content: res.answer || 'No response' }]);
      },
      error: () => {
        const updated = this.messagesSubject.value;
        this.messagesSubject.next([...updated, { role: 'assistant', content: 'Error sending message' }]);
      }
    })
  }
}
