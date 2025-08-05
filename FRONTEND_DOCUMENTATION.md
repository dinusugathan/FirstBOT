# Frontend Documentation - EduChat Interface

## Overview

The EduChat frontend is a modern, responsive chat interface built with HTML, CSS (Tailwind), and vanilla JavaScript. It provides an intuitive user experience for course inquiries and translation services.

## File Structure

```
templates/
└── index.html (551 lines) - Main chat interface
```

## Technology Stack

- **HTML5**: Semantic markup structure
- **Tailwind CSS**: Utility-first CSS framework via CDN
- **Google Fonts**: Poppins font family for modern typography
- **Vanilla JavaScript**: Client-side functionality and API interactions

## Design System

### Color Scheme

- **Background**: Linear gradient from `#f5f7fa` to `#c3cfe2`
- **Primary**: Blue tones for system messages and buttons
- **Secondary**: Green tones for user messages
- **Accent**: Purple/pink gradients for interactive elements

### Typography

- **Font Family**: 'Poppins' with weights: 300, 400, 500, 600
- **Responsive Text**: Scales appropriately across device sizes

### Animations

1. **Fade In Animation**:
   ```css
   @keyframes fadeIn {
       from { opacity: 0; transform: translateY(10px); }
       to { opacity: 1; transform: translateY(0); }
   }
   ```

2. **Float Animation**:
   ```css
   @keyframes float {
       0% { transform: translateY(0px); }
       50% { transform: translateY(-5px); }
       100% { transform: translateY(0px); }
   }
   ```

## Component Architecture

### 1. Chat Container

**Structure**: Main chat interface container with responsive layout

**Features**:
- Centered layout with maximum width constraints
- Responsive height adjustment
- Shadow effects for depth
- Rounded corners for modern appearance

**CSS Classes**:
```css
.chat-container {
    max-width: 800px;
    height: 600px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
```

### 2. Chat Header

**Elements**:
- Application title: "EduChat"
- Subtitle: "Course Enquiry Assistant"
- Floating animation effect

**Styling**:
- Gradient background
- Centered text alignment
- Padding for breathing room

### 3. Messages Container

**Purpose**: Scrollable area for displaying conversation history

**Features**:
- Auto-scroll to bottom on new messages
- Overflow handling for long conversations
- Responsive height calculation

**JavaScript Functions**:
```javascript
function scrollToBottom() {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
```

### 4. Message Components

#### User Messages

**Styling**:
- Right-aligned with green gradient background
- Rounded corners with tail indicator
- White text for contrast

**CSS Structure**:
```css
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    align-self: flex-end;
    border-radius: 18px 18px 5px 18px;
}
```

#### Bot Messages

**Styling**:
- Left-aligned with blue gradient background
- Rounded corners with tail indicator
- White text for readability

**CSS Structure**:
```css
.bot-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    align-self: flex-start;
    border-radius: 18px 18px 18px 5px;
}
```

### 5. Input Area

**Components**:
- Text input field for user queries
- Send button with icon
- Translation toggle button
- Language selector dropdown

**Features**:
- Enter key submission
- Input validation
- Loading states during processing

### 6. Translation Interface

**Elements**:
- Language selection dropdown
- Translation toggle button
- Integrated workflow with main chat

**Supported Languages**:
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## JavaScript Functionality

### Core Functions

#### 1. sendMessage()

**Purpose**: Handles user message submission and API communication

**Process**:
1. Validates input
2. Displays user message
3. Shows loading indicator
4. Calls appropriate API endpoint
5. Displays response
6. Clears input field

```javascript
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: message,
                conversationId: conversationId
            })
        });
        
        const data = await response.json();
        hideLoading();
        addMessage(data.response, 'bot');
    } catch (error) {
        hideLoading();
        addMessage('Sorry, something went wrong. Please try again.', 'bot');
    }
}
```

#### 2. translateMessage()

**Purpose**: Handles text translation requests

**Process**:
1. Gets text from input or last bot message
2. Validates translation parameters
3. Calls translation API
4. Displays translated result

```javascript
async function translateMessage() {
    const userInput = document.getElementById('userInput');
    const targetLang = document.getElementById('languageSelect').value;
    let textToTranslate = userInput.value.trim();
    
    // If no input, translate last bot message
    if (!textToTranslate) {
        const messages = document.querySelectorAll('.bot-message');
        if (messages.length > 0) {
            textToTranslate = messages[messages.length - 1].textContent;
        }
    }
    
    if (!textToTranslate) {
        addMessage('Please enter text to translate or have a conversation first.', 'bot');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: textToTranslate,
                target_lang: targetLang,
                conversationId: conversationId
            })
        });
        
        const data = await response.json();
        hideLoading();
        addMessage(`Translation (${targetLang}): ${data.translation}`, 'bot');
    } catch (error) {
        hideLoading();
        addMessage('Translation failed. Please try again.', 'bot');
    }
}
```

#### 3. addMessage(message, sender)

**Purpose**: Adds messages to the chat interface

**Parameters**:
- `message` (string): The message content
- `sender` (string): Either 'user' or 'bot'

**Features**:
- Creates appropriate message styling
- Adds fade-in animation
- Auto-scrolls to bottom

```javascript
function addMessage(message, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    
    messageDiv.className = `message ${sender}-message animate-fade-in`;
    messageDiv.textContent = message;
    
    // Add message tail
    const tail = document.createElement('div');
    tail.className = `message-tail ${sender}-message-tail bg-gradient-to-r from-blue-500 to-purple-600`;
    messageDiv.appendChild(tail);
    
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}
```

#### 4. Loading States

**Functions**:
- `showLoading()`: Displays typing indicator
- `hideLoading()`: Removes typing indicator

```javascript
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading';
    loadingDiv.className = 'message bot-message animate-fade-in';
    loadingDiv.innerHTML = `
        <div class="flex space-x-1">
            <div class="w-2 h-2 bg-white rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
    `;
    
    document.getElementById('messages').appendChild(loadingDiv);
    scrollToBottom();
}
```

### Event Handlers

#### 1. Enter Key Submission

```javascript
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
```

#### 2. Button Click Handlers

```javascript
document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('translateBtn').addEventListener('click', translateMessage);
```

## Responsive Design

### Mobile Optimization

- **Viewport Meta Tag**: Ensures proper scaling on mobile devices
- **Flexible Layouts**: Uses Flexbox for responsive component arrangement
- **Touch-Friendly**: Button sizes optimized for touch interaction
- **Font Scaling**: Responsive typography that scales with screen size

### Breakpoint Considerations

- **Small Screens** (< 768px): Single column layout, full-width components
- **Medium Screens** (768px - 1024px): Optimized spacing and sizing
- **Large Screens** (> 1024px): Maximum width constraints, centered layout

## Accessibility Features

### Semantic HTML

- Proper heading hierarchy
- Form labels and associations
- ARIA attributes where appropriate

### Keyboard Navigation

- Tab order follows logical flow
- Enter key submission for forms
- Focus indicators for interactive elements

### Screen Reader Support

- Alt text for images and icons
- Descriptive button labels
- Proper form labeling

## Performance Optimizations

### CSS Optimizations

- **Tailwind CDN**: Reduces bundle size
- **CSS Animations**: Hardware-accelerated transforms
- **Minimal Custom CSS**: Leverages utility classes

### JavaScript Optimizations

- **Vanilla JS**: No framework overhead
- **Async/Await**: Non-blocking API calls
- **Event Delegation**: Efficient event handling

### Loading Optimizations

- **Font Display**: Optimized Google Fonts loading
- **Lazy Loading**: Messages loaded as needed
- **Debounced Input**: Prevents excessive API calls

## Browser Compatibility

### Supported Browsers

- **Chrome**: 88+
- **Firefox**: 85+
- **Safari**: 14+
- **Edge**: 88+

### Feature Support

- **CSS Grid**: Used for layout
- **Flexbox**: Component arrangement
- **CSS Animations**: Smooth transitions
- **Fetch API**: Modern AJAX requests

## Customization Guide

### Theming

1. **Colors**: Modify gradient definitions in CSS
2. **Fonts**: Change font imports and family declarations
3. **Spacing**: Adjust Tailwind utility classes
4. **Animations**: Modify keyframe definitions

### Adding Features

1. **New Message Types**: Extend `addMessage()` function
2. **Additional Languages**: Update language selector options
3. **Custom Styling**: Add new CSS classes
4. **Enhanced Interactions**: Extend JavaScript functionality

## Testing Recommendations

### Manual Testing

1. **Message Flow**: Test complete conversation cycles
2. **Translation**: Verify all language options
3. **Error Handling**: Test network failures and invalid inputs
4. **Responsive**: Test across different screen sizes

### Automated Testing

```javascript
// Example test structure
describe('Chat Interface', () => {
    test('should send message on Enter key', () => {
        // Test implementation
    });
    
    test('should handle translation requests', () => {
        // Test implementation
    });
    
    test('should display loading states', () => {
        // Test implementation
    });
});
```

## Future Enhancements

### Potential Features

1. **File Upload**: Support for document attachments
2. **Voice Input**: Speech-to-text functionality
3. **Message History**: Persistent conversation storage
4. **Rich Text**: Markdown support for formatted responses
5. **Emoji Support**: Enhanced expression options
6. **Dark Mode**: Alternative color scheme
7. **Notification System**: Browser notifications for responses

### Technical Improvements

1. **WebSocket Integration**: Real-time communication
2. **Progressive Web App**: Offline functionality
3. **Component Framework**: Migration to React/Vue
4. **State Management**: Centralized state handling
5. **Unit Testing**: Comprehensive test coverage

## Troubleshooting

### Common Issues

1. **Messages Not Displaying**: Check API connectivity
2. **Styling Issues**: Verify Tailwind CSS loading
3. **Translation Errors**: Validate language codes
4. **Mobile Layout**: Test viewport meta tag

### Debug Tools

1. **Browser DevTools**: Network tab for API calls
2. **Console Logging**: Add debug statements
3. **Responsive Testing**: Device simulation
4. **Performance Profiling**: Identify bottlenecks