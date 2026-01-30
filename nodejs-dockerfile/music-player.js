const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// Configuration
const PORT = process.env.PORT || 8080;
const DATA_FILE = './music-data.json';

// Initialize data file
if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify({
        songs: [],
        playlists: [],
        stats: {
            totalPlays: 0,
            totalSongs: 0,
            totalDuration: 0,
            favoriteGenre: "Pop"
        }
    }, null, 2));
}

// Color scheme
const COLORS = {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    success: '#10b981',
    danger: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6',
    dark: '#0f172a',
    light: '#f8fafc'
};

// Sample music data
const SAMPLE_SONGS = [
    {
        id: 1,
        title: "Midnight City",
        artist: "M83",
        album: "Hurry Up, We're Dreaming",
        genre: "Electronic",
        duration: "4:04",
        plays: 245,
        rating: 4.8,
        color: "#8b5cf6",
        waveform: [30, 60, 40, 80, 30, 70, 50, 90, 40, 60]
    },
    {
        id: 2,
        title: "Blinding Lights",
        artist: "The Weeknd",
        album: "After Hours",
        genre: "R&B",
        duration: "3:22",
        plays: 189,
        rating: 4.9,
        color: "#ef4444",
        waveform: [40, 70, 50, 85, 45, 75, 55, 95, 50, 70]
    },
    {
        id: 3,
        title: "Levitating",
        artist: "Dua Lipa",
        album: "Future Nostalgia",
        genre: "Pop",
        duration: "3:24",
        plays: 167,
        rating: 4.7,
        color: "#f59e0b",
        waveform: [35, 65, 45, 75, 40, 70, 55, 85, 45, 65]
    },
    {
        id: 4,
        title: "good 4 u",
        artist: "Olivia Rodrigo",
        album: "SOUR",
        genre: "Pop Rock",
        duration: "2:58",
        plays: 154,
        rating: 4.6,
        color: "#10b981",
        waveform: [45, 75, 55, 85, 50, 80, 60, 90, 55, 75]
    },
    {
        id: 5,
        title: "Stay",
        artist: "The Kid LAROI, Justin Bieber",
        album: "F*CK LOVE 3",
        genre: "Pop",
        duration: "2:21",
        plays: 132,
        rating: 4.5,
        color: "#3b82f6",
        waveform: [30, 60, 40, 70, 35, 65, 45, 75, 40, 60]
    },
    {
        id: 6,
        title: "Heat Waves",
        artist: "Glass Animals",
        album: "Dreamland",
        genre: "Indie Pop",
        duration: "3:59",
        plays: 178,
        rating: 4.8,
        color: "#ec4899",
        waveform: [40, 70, 50, 80, 45, 75, 55, 85, 50, 70]
    }
];

// Initialize with sample data if empty
const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
if (data.songs.length === 0) {
    data.songs = SAMPLE_SONGS;
    data.stats.totalSongs = SAMPLE_SONGS.length;
    data.stats.totalPlays = SAMPLE_SONGS.reduce((sum, song) => sum + song.plays, 0);
    data.stats.totalDuration = "1:45:20";
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// CSS Styles
const STYLES = `
    <style>
        :root {
            --primary: ${COLORS.primary};
            --secondary: ${COLORS.secondary};
            --success: ${COLORS.success};
            --danger: ${COLORS.danger};
            --warning: ${COLORS.warning};
            --info: ${COLORS.info};
            --dark: #0f172a;
            --light: #f8fafc;
            --gray-800: #1e293b;
            --gray-700: #334155;
            --gray-600: #475569;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            
            /* Gradients */
            --gradient-primary: linear-gradient(135deg, ${COLORS.primary}, ${COLORS.secondary});
            --gradient-danger: linear-gradient(135deg, #f97316, ${COLORS.danger});
            --gradient-success: linear-gradient(135deg, ${COLORS.success}, #22d3ee);
            --gradient-warning: linear-gradient(135deg, ${COLORS.warning}, #f59e0b);
            
            /* Shadows */
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
            --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            
            /* Border Radius */
            --radius-lg: 1rem;
            --radius-md: 0.75rem;
            --radius-sm: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--dark);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(245, 158, 11, 0.1) 0%, transparent 30%);
        }
        
        /* Header */
        .header {
            background: var(--gradient-primary);
            padding: 2rem 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
            border-bottom: 3px solid rgba(255, 255, 255, 0.1);
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .header h1 {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #f1f5f9, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            letter-spacing: -0.5px;
        }
        
        .header p {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.9);
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        /* Grid */
        .grid {
            display: grid;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        
        /* Cards */
        .card {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-lg);
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary);
        }
        
        .card.gradient {
            background: var(--gradient-primary);
            color: white;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        /* Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            border-color: var(--primary);
            background: rgba(255, 255, 255, 0.08);
        }
        
        .stat-card:nth-child(1) { border-top: 4px solid var(--primary); }
        .stat-card:nth-child(2) { border-top: 4px solid var(--danger); }
        .stat-card:nth-child(3) { border-top: 4px solid var(--success); }
        .stat-card:nth-child(4) { border-top: 4px solid var(--warning); }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0.5rem 0;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Music Player */
        .player {
            background: var(--gradient-primary);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }
        
        .player::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></svg>');
            opacity: 0.3;
        }
        
        .now-playing {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .album-art {
            width: 120px;
            height: 120px;
            border-radius: var(--radius-md);
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .song-info h3 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: white;
        }
        
        .song-info p {
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 0.5rem;
        }
        
        .song-rating {
            color: #fbbf24;
            font-size: 1.2rem;
        }
        
        /* Waveform */
        .waveform {
            display: flex;
            align-items: center;
            gap: 4px;
            height: 60px;
            margin: 1.5rem 0;
        }
        
        .wave-bar {
            flex: 1;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            min-height: 10px;
            transition: all 0.3s ease;
        }
        
        .wave-bar.active {
            background: white;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        /* Controls */
        .controls {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .control-btn {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .control-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }
        
        .control-btn.play {
            width: 70px;
            height: 70px;
            background: white;
            color: var(--primary);
            font-size: 1.5rem;
        }
        
        .control-btn.play:hover {
            background: rgba(255, 255, 255, 0.9);
            transform: scale(1.15);
        }
        
        /* Progress */
        .progress-container {
            width: 100%;
            margin-top: 1.5rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }
        
        .progress {
            height: 100%;
            background: white;
            width: 45%;
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        .time-display {
            display: flex;
            justify-content: space-between;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.875rem;
        }
        
        /* Song List */
        .song-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        
        .song-item {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-md);
            padding: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.3s ease;
            border-left: 4px solid;
            cursor: pointer;
        }
        
        .song-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .song-item.playing {
            background: rgba(99, 102, 241, 0.2);
            border-left-color: var(--primary);
        }
        
        .song-number {
            width: 30px;
            height: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
        }
        
        .song-item.playing .song-number {
            background: var(--primary);
            color: white;
        }
        
        .song-details {
            flex: 1;
        }
        
        .song-details h4 {
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
            color: var(--text-primary);
        }
        
        .song-details p {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        .song-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        .song-plays {
            color: var(--warning);
        }
        
        .song-duration {
            color: var(--info);
        }
        
        /* Genres */
        .genres {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
        }
        
        .genre-tag {
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-full);
            font-size: 0.875rem;
            color: var(--text-secondary);
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        
        .genre-tag:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        
        .genre-tag.active {
            background: var(--primary);
            color: white;
        }
        
        /* Charts */
        .chart-container {
            background: rgba(30, 41, 59, 0.8);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .grid-4, .grid-3 {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
        }
        
        @media (max-width: 768px) {
            .grid-4, .grid-3, .grid-2 {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .now-playing {
                flex-direction: column;
                text-align: center;
            }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out forwards;
        }
        
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.2s; }
        .delay-3 { animation-delay: 0.3s; }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--dark);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--gradient-primary);
            border-radius: var(--radius-full);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--primary), var(--danger));
        }
    </style>
`;

// JavaScript
const SCRIPT = `
    <script>
        let currentSong = 1;
        let isPlaying = false;
        let progressInterval;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updatePlayer();
            updateTime();
            setInterval(updateTime, 1000);
            
            // Event listeners
            document.querySelectorAll('.song-item').forEach(item => {
                item.addEventListener('click', function() {
                    const songId = parseInt(this.dataset.id);
                    playSong(songId);
                });
            });
            
            // Control buttons
            document.getElementById('play-btn').addEventListener('click', togglePlay);
            document.getElementById('prev-btn').addEventListener('click', prevSong);
            document.getElementById('next-btn').addEventListener('click', nextSong);
            
            // Genre filter
            document.querySelectorAll('.genre-tag').forEach(tag => {
                tag.addEventListener('click', function() {
                    const genre = this.dataset.genre;
                    filterSongs(genre);
                    
                    // Update active state
                    document.querySelectorAll('.genre-tag').forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                });
            });
            
            // Reset filter
            document.getElementById('reset-filter').addEventListener('click', function() {
                filterSongs('all');
                document.querySelectorAll('.genre-tag').forEach(t => t.classList.remove('active'));
            });
            
            // Simulate waveform animation
            animateWaveform();
        });
        
        function playSong(songId) {
            currentSong = songId;
            updatePlayer();
            
            if (!isPlaying) {
                togglePlay();
            }
        }
        
        function togglePlay() {
            isPlaying = !isPlaying;
            const playBtn = document.getElementById('play-btn');
            const icon = playBtn.querySelector('i');
            
            if (isPlaying) {
                icon.className = 'fas fa-pause';
                startProgress();
                animateWaveform();
            } else {
                icon.className = 'fas fa-play';
                stopProgress();
            }
        }
        
        function prevSong() {
            currentSong = currentSong > 1 ? currentSong - 1 : ${data.songs.length};
            updatePlayer();
        }
        
        function nextSong() {
            currentSong = currentSong < ${data.songs.length} ? currentSong + 1 : 1;
            updatePlayer();
        }
        
        function updatePlayer() {
            const song = songs.find(s => s.id === currentSong);
            if (!song) return;
            
            // Update now playing
            document.getElementById('now-playing-title').textContent = song.title;
            document.getElementById('now-playing-artist').textContent = song.artist;
            document.getElementById('now-playing-album').textContent = song.album;
            document.getElementById('now-playing-rating').innerHTML = '★'.repeat(Math.floor(song.rating)) + '☆'.repeat(5 - Math.floor(song.rating));
            
            // Update album art color
            const albumArt = document.querySelector('.album-art');
            albumArt.style.background = \`linear-gradient(135deg, \${song.color}, \${darkenColor(song.color)})\`;
            albumArt.innerHTML = \`<i class="fas fa-music"></i>\`;
            
            // Update waveform
            updateWaveform(song.waveform);
            
            // Update song list
            document.querySelectorAll('.song-item').forEach(item => {
                item.classList.toggle('playing', parseInt(item.dataset.id) === currentSong);
            });
            
            // Update stats
            updateStats();
        }
        
        function updateWaveform(waveform) {
            const wavebars = document.querySelectorAll('.wave-bar');
            wavebars.forEach((bar, index) => {
                const height = waveform[index % waveform.length];
                bar.style.height = \`\${height}%\`;
            });
        }
        
        function animateWaveform() {
            if (!isPlaying) return;
            
            const wavebars = document.querySelectorAll('.wave-bar');
            wavebars.forEach((bar, index) => {
                setTimeout(() => {
                    bar.classList.add('active');
                    setTimeout(() => bar.classList.remove('active'), 300);
                }, index * 50);
            });
            
            setTimeout(animateWaveform, 1000);
        }
        
        function startProgress() {
            let progress = 0;
            progressInterval = setInterval(() => {
                if (progress >= 100) {
                    progress = 0;
                    nextSong();
                }
                progress += 0.5;
                document.querySelector('.progress').style.width = \`\${progress}%\`;
                
                // Update time display
                const currentTime = formatTime(progress * 2.16); // 2.16 seconds per percent for 3:36 song
                const totalTime = "3:36";
                document.getElementById('current-time').textContent = currentTime;
                document.getElementById('total-time').textContent = totalTime;
            }, 100);
        }
        
        function stopProgress() {
            clearInterval(progressInterval);
        }
        
        function filterSongs(genre) {
            document.querySelectorAll('.song-item').forEach(item => {
                const songGenre = item.dataset.genre;
                item.style.display = (genre === 'all' || songGenre === genre) ? 'flex' : 'none';
            });
        }
        
        function updateStats() {
            const totalPlays = songs.reduce((sum, song) => sum + song.plays, 0);
            const avgRating = (songs.reduce((sum, song) => sum + song.rating, 0) / songs.length).toFixed(1);
            
            document.getElementById('total-plays').textContent = totalPlays.toLocaleString();
            document.getElementById('avg-rating').innerHTML = \`\${avgRating} <span style="color: #fbbf24">★</span>\`;
            document.getElementById('total-songs').textContent = songs.length;
            
            // Update genre distribution
            const genreCount = {};
            songs.forEach(song => {
                genreCount[song.genre] = (genreCount[song.genre] || 0) + 1;
            });
            
            const genreList = document.getElementById('genre-list');
            genreList.innerHTML = Object.entries(genreCount)
                .sort((a, b) => b[1] - a[1])
                .map(([genre, count]) => \`
                    <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                        <span>\${genre}</span>
                        <span style="color: var(--warning)">\${count}</span>
                    </div>
                \`).join('');
        }
        
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            document.getElementById('current-time-display').textContent = timeString;
            
            const dateString = now.toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            document.getElementById('current-date').textContent = dateString;
        }
        
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return \`\${mins}:\${secs.toString().padStart(2, '0')}\`;
        }
        
        function darkenColor(color) {
            // Simple color darkening
            return color.replace(/\\d+/g, num => Math.max(0, parseInt(num) - 40));
        }
        
        // Songs data from server
        const songs = ${JSON.stringify(data.songs)};
        
        // Initial update
        updateStats();
    </script>
`;

// HTML Template
function generateHTML() {
    const songs = data.songs;
    const stats = data.stats;
    
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🎵 VibeWave Music Player</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            ${STYLES}
            <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎵</text></svg>">
        </head>
        <body>
            <!-- Header -->
            <header class="header fade-in">
                <div class="container">
                    <h1><i class="fas fa-headphones-alt"></i> VibeWave Music Player</h1>
                    <p>Immersive music experience with stunning visualizations and analytics</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                        <i class="fas fa-clock"></i> <span id="current-time-display">Loading...</span> • 
                        <i class="fas fa-calendar"></i> <span id="current-date">Loading...</span>
                    </div>
                </div>
            </header>

            <main class="container">
                <!-- Stats -->
                <div class="stats-grid fade-in delay-1">
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-play-circle"></i></div>
                        <div class="stat-value" id="total-plays">${stats.totalPlays.toLocaleString()}</div>
                        <div class="stat-label">Total Plays</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-star"></i></div>
                        <div class="stat-value" id="avg-rating">4.7 <span style="color: #fbbf24">★</span></div>
                        <div class="stat-label">Avg Rating</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-music"></i></div>
                        <div class="stat-value" id="total-songs">${songs.length}</div>
                        <div class="stat-label">Total Songs</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-clock"></i></div>
                        <div class="stat-value">${stats.totalDuration}</div>
                        <div class="stat-label">Total Duration</div>
                    </div>
                </div>

                <!-- Main Player -->
                <div class="player fade-in delay-2">
                    <div class="now-playing">
                        <div class="album-art">
                            <i class="fas fa-music"></i>
                        </div>
                        <div class="song-info">
                            <h3 id="now-playing-title">${songs[0].title}</h3>
                            <p id="now-playing-artist"><i class="fas fa-user"></i> ${songs[0].artist}</p>
                            <p id="now-playing-album"><i class="fas fa-compact-disc"></i> ${songs[0].album}</p>
                            <div class="song-rating" id="now-playing-rating">${'★'.repeat(Math.floor(songs[0].rating))}${'☆'.repeat(5 - Math.floor(songs[0].rating))}</div>
                        </div>
                    </div>
                    
                    <!-- Waveform -->
                    <div class="waveform" id="waveform">
                        ${Array.from({ length: 20 }, (_, i) => 
                            `<div class="wave-bar" style="height: ${songs[0].waveform[i % songs[0].waveform.length]}%"></div>`
                        ).join('')}
                    </div>
                    
                    <!-- Progress -->
                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress"></div>
                        </div>
                        <div class="time-display">
                            <span id="current-time">0:00</span>
                            <span id="total-time">3:36</span>
                        </div>
                    </div>
                    
                    <!-- Controls -->
                    <div class="controls">
                        <button class="control-btn" id="shuffle-btn">
                            <i class="fas fa-random"></i>
                        </button>
                        <button class="control-btn" id="prev-btn">
                            <i class="fas fa-step-backward"></i>
                        </button>
                        <button class="control-btn play" id="play-btn">
                            <i class="fas fa-play"></i>
                        </button>
                        <button class="control-btn" id="next-btn">
                            <i class="fas fa-step-forward"></i>
                        </button>
                        <button class="control-btn" id="repeat-btn">
                            <i class="fas fa-redo"></i>
                        </button>
                    </div>
                </div>

                <!-- Main Content Grid -->
                <div class="grid grid-3 fade-in delay-3">
                    <!-- Song Library -->
                    <div class="card" style="grid-column: span 2;">
                        <div class="card-header">
                            <h2 class="card-title"><i class="fas fa-list-music"></i> Song Library</h2>
                            <div>
                                <button class="genre-tag active" data-genre="all" id="reset-filter">All Genres</button>
                                ${[...new Set(songs.map(s => s.genre))].map(genre => 
                                    `<button class="genre-tag" data-genre="${genre}">${genre}</button>`
                                ).join('')}
                            </div>
                        </div>
                        <div class="song-list">
                            ${songs.map((song, index) => `
                                <div class="song-item ${index === 0 ? 'playing' : ''}" data-id="${song.id}" data-genre="${song.genre}">
                                    <div class="song-number">${index + 1}</div>
                                    <div class="song-details">
                                        <h4>${song.title}</h4>
                                        <p>${song.artist} • ${song.album}</p>
                                        <div class="song-meta">
                                            <span class="song-plays"><i class="fas fa-play"></i> ${song.plays}</span>
                                            <span class="song-duration"><i class="fas fa-clock"></i> ${song.duration}</span>
                                            <span style="color: ${song.color}"><i class="fas fa-circle"></i> ${song.genre}</span>
                                        </div>
                                    </div>
                                    <div style="color: #fbbf24">
                                        ${'★'.repeat(Math.floor(song.rating))}${'☆'.repeat(5 - Math.floor(song.rating))}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Genre Analytics -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title"><i class="fas fa-chart-pie"></i> Genre Distribution</h2>
                        </div>
                        <div id="genre-list">
                            ${Object.entries(
                                songs.reduce((acc, song) => {
                                    acc[song.genre] = (acc[song.genre] || 0) + 1;
                                    return acc;
                                }, {})
                            ).sort((a, b) => b[1] - a[1]).map(([genre, count]) => `
                                <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                                    <span>${genre}</span>
                                    <span style="color: var(--warning)">${count}</span>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div style="margin-top: 1.5rem;">
                            <h3 style="margin-bottom: 1rem;"><i class="fas fa-fire"></i> Top Songs</h3>
                            ${songs.sort((a, b) => b.plays - a.plays).slice(0, 3).map(song => `
                                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(255,255,255,0.05); border-radius: var(--radius-sm);">
                                    <div style="width: 30px; height: 30px; background: ${song.color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: white;">${song.plays}</div>
                                    <div>
                                        <div style="font-weight: 600;">${song.title}</div>
                                        <div style="font-size: 0.875rem; color: var(--text-muted);">${song.artist}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Player Stats -->
                    <div class="card gradient">
                        <div class="card-header">
                            <h2 class="card-title"><i class="fas fa-chart-line"></i> Player Stats</h2>
                        </div>
                        <div style="text-align: center; padding: 1rem;">
                            <div style="font-size: 4rem; margin-bottom: 1rem;">
                                <i class="fas fa-wave-square"></i>
                            </div>
                            <h3 style="margin-bottom: 0.5rem;">Active Listening</h3>
                            <p style="opacity: 0.9;">Real-time audio visualization and analytics</p>
                        </div>
                    </div>

                    <!-- Equalizer -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title"><i class="fas fa-sliders-h"></i> Equalizer</h2>
                        </div>
                        <div style="padding: 1rem;">
                            ${['Bass', 'Mid', 'Treble'].map((band, i) => `
                                <div style="margin-bottom: 1rem;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                        <span>${band}</span>
                                        <span>${[60, 45, 75][i]}%</span>
                                    </div>
                                    <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                                        <div style="height: 100%; width: ${[60, 45, 75][i]}%; background: var(--primary); border-radius: 4px;"></div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Recent Activity -->
                    <div class="card" style="grid-column: span 2;">
                        <div class="card-header">
                            <h2 class="card-title"><i class="fas fa-history"></i> Recent Activity</h2>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem;">
                            ${songs.slice(0, 4).map(song => `
                                <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: var(--radius-md); border-left: 4px solid ${song.color};">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                                        <div style="width: 40px; height: 40px; background: ${song.color}; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: white;">
                                            <i class="fas fa-music"></i>
                                        </div>
                                        <div>
                                            <div style="font-weight: 600;">${song.title}</div>
                                            <div style="font-size: 0.875rem; color: var(--text-muted);">${song.artist}</div>
                                        </div>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.875rem;">
                                        <span><i class="fas fa-play" style="color: var(--warning);"></i> ${song.plays} plays</span>
                                        <span><i class="fas fa-clock" style="color: var(--info);"></i> ${song.duration}</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </main>

            <!-- Footer -->
            <footer class="footer">
                <p><i class="fas fa-heart" style="color: var(--danger);"></i> VibeWave Music Player v1.0 • Built with Node.js & HTML/CSS/JS</p>
                <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                    <i class="fas fa-server"></i> Server running on port ${PORT} • 
                    <i class="fas fa-database"></i> ${songs.length} songs loaded • 
                    <i class="fas fa-code"></i> Single-file application
                </p>
            </footer>

            ${SCRIPT}
        </body>
        </html>
    `;
}

// Create HTTP server
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // API endpoints
    if (parsedUrl.pathname === '/api/songs') {
        if (req.method === 'GET') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(data.songs));
            return;
        }
    } else if (parsedUrl.pathname === '/api/stats') {
        if (req.method === 'GET') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(data.stats));
            return;
        }
    } else if (parsedUrl.pathname === '/api/play') {
        if (req.method === 'POST') {
            let body = '';
            req.on('data', chunk => body += chunk);
            req.on('end', () => {
                const { songId } = JSON.parse(body);
                const song = data.songs.find(s => s.id === songId);
                if (song) {
                    song.plays++;
                    data.stats.totalPlays++;
                    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
                }
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
            });
            return;
        }
    }
    
    // Serve HTML for all other routes
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(generateHTML());
});

// Start server
server.listen(PORT, () => {
    console.log(`\n🎵 ${'='.repeat(50)}`);
    console.log(`   VibeWave Music Player`);
    console.log(`   ${'='.repeat(50)}`);
    console.log(`   Server running at: http://localhost:${PORT}`);
    console.log(`   Songs loaded: ${data.songs.length}`);
    console.log(`   Total plays: ${data.stats.totalPlays}`);
    console.log(`   ${'='.repeat(50)}`);
    console.log(`   🎧 Enjoy your music! 🎧`);
    console.log(`${'='.repeat(50)}\n`);
});
