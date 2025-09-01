export class ChatRequest {
    question: string;

    constructor(question: string) {
        this.question = question;
    }
}

export class ChatResponse {
    response: string;

    constructor(response: string) {
        this.response = response;
    }
}