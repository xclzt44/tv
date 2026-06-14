import requests
import re

# إعدادات المواقع والمصادر
SOURCES = {
    "Yallo_TV_Serv1": {
        "page_url": "https://new.marocan.xyz/albaplayer/yallo1/?serv=1",
        "referer": "https://new.marocan.xyz/",
        "display_name": "Yallo TV - سيرفر 1"
    },
    "Fastly_Live_Serv2": {
        "page_url": "https://new.marocan.xyz/albaplayer/yallo1/?serv=2",
        "referer": "",
        "display_name": "Fastly Live - سيرفر 2"
    }
}

USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"

def fetch_live_link(source_key, info):
    headers = {"User-Agent": USER_AGENT}
    if info["referer"]:
        headers["Referer"] = info["referer"]
    try:
        response = requests.get(info["page_url"], headers=headers, timeout=15)
        if response.status_code == 200:
            html = response.text
            links = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', html)
            if links:
                for link in links:
                    if source_key == "Yallo_TV_Serv1" and ("kooran" in link or "tist2" in link):
                        return link
                    if source_key == "Fastly_Live_Serv2" and "pscp.tv" in link:
                        return link
                return links[0]
        return None
    except:
        return None

def generate_iptv_playlist():
    m3u_output = "#EXTM3U\n\n"
    for key, info in SOURCES.items():
        live_url = fetch_live_link(key, info)
        if not live_url:
            if key == "Yallo_TV_Serv1":
                live_url = "https://live.kooran13.cfd/tist2/index.m3u8"
            elif key == "Fastly_Live_Serv2":
                live_url = "https://prod-fastly-eu-central-1.video.pscp.tv/Transcoding/v1/hls/0ujF4lpQzwXiGWBQGV81drLdPzCR_3JKg6eF7WvWQkSLwymVJQqCNAQ0dy1_qQ5pK0zEyd2Glb5ir7uINL7UYA/transcode/eu-central-1/periscope-replay-direct-prod-eu-central-1-public/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsInZlcnNpb24iOiIyIn0.eyJFbmNvZGVyU2V0dGluZyI6ImVuY29kZXJfc2V0dGluZ18xMDgwcDYwXzEwIiwiSGVpZ2h0IjoxMDgwLCJIaWdoRnJhbWVSYXRlIjp0cnVlLCJLYnBzIjo4MDAwLCJXaWR0aCI6MTkyMH0.OBq8EsoF4c8ydlmfZFxJzACPHYFjmjUaSER2wvsfHso/dynamic_delta.m3u8?type=live&_HLS_skip=YES"

        m3u_output += f'#EXTINF:-1 tvg-id="{key}" tvg-name="{info["display_name"]}" group-title="Sports", {info["display_name"]}\n'
        m3u_output += f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n'
        if info["referer"]:
            m3u_output += f'#EXTVLCOPT:http-referrer={info["referer"]}\n'
        m3u_output += f'{live_url}\n\n'

    with open("live_sports.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output.strip())

if __name__ == "__main__":
    generate_iptv_playlist()
