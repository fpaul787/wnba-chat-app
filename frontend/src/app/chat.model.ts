export class ChatRequest {
    question: string;

    constructor(question: string) {
        this.question = question;
    }
}

export class ChatResponse {
    answer: string;

    constructor(answer: string) {
        this.answer = answer;
    }
}