Homelab  
A self-hosted infrastructure running a static portfolio website from a residential server behind CGNAT, published to the internet through a VPS using a WireGuard reverse tunnel.
Architecture  
Internet  
│  
▼  
[VPS - Oracle Cloud]  
├── Nginx (Reverse Proxy + HTTPS)  → Docker  
├── Certbot (Let's Encrypt)        → Docker  
└── WireGuard (UDP Tunnel)         → Native  
│  
▼ WireGuard Tunnel  
│  
[Residential Server - Behind CGNAT]  
├── Nginx (Static File Server)     → Docker  
└── WireGuard (Client)             → Native  
Tech Stack  

Docker + Docker Compose — Container orchestration  
Nginx — Reverse proxy (VPS) and static file server (local)  
Let's Encrypt + Certbot — Automated TLS certificates  
WireGuard — Encrypted tunnel to bypass CGNAT  
Ubuntu Server — Host OS on both machines  
Git — Infrastructure versioning  

Project Structure  
homelab/  
├── vps/  
│   ├── docker-compose.yml  
│   └── nginx/  
│       └── default.conf  
└── portfolio/  
    ├── docker-compose.yml  
    ├── Dockerfile  
    └── site/  
