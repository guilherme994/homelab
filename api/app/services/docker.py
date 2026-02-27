import docker


def get_containers_status():
    client = docker.DockerClient(base_url="unix:///var/run/docker.sock")

    containers = client.containers.list(all=True)

    result = []
    for container in containers:
        attrs = container.attrs
        state = attrs["State"]

        result.append({
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else "unknown",
            "status": container.status,
            "started_at": state.get("StartedAt", ""),
            "health": state.get("Health", {}).get("Status", "N/A"),
        })

    client.close()
    return result
