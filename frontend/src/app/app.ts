import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('wnba-chat');

  userMessage = '';

  ngOnInit() {
    // Initialize user message or perform any setup logic here
  }

  sendMessage(){
    const query = this.userMessage.trim();
  }
}
