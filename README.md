# Flastagram

Flastagram is a social media application inspired by BeReal. This platform is designed exclusively for college events organized by your organization, enabling users to share their moments in a community-focused environment.

## Features

- **Event-Centric Posts**: Share photos and moments specifically tied to college events.
- **Real-Time Updates**: Stay updated with live feeds from your organization’s activities.
- **User Profiles**: Create and manage profiles showcasing participation in events.
- **Event Discovery**: Explore ongoing and upcoming college events.

## Tech Stack

- **Frontend**: React.js
- **Backend**: Express.js
- **Database**: MongoDB
- **Real-Time Communication**: Socket.IO
- **Hosting**: [Specify your hosting platform, e.g., Heroku, Vercel, etc.]

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Node.js (v14 or higher)
- npm (v6 or higher)
- MongoDB (local or cloud instance)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hyeonsooko/flastagram.git
   cd flastagram
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory and add the following:
   ```env
   MONGO_URI=<your_mongodb_connection_string>
   PORT=5000
   SOCKET_PORT=5001
   ```

4. Run the development server:
   ```bash
   npm start
   ```

5. Open your browser and navigate to `http://localhost:5000`.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

[MIT License](LICENSE)

## Contact

For questions or collaboration:

- **Sooko**
- GitHub: [@hyeonsooko](https://github.com/hyeonsooko)
