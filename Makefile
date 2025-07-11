
rebuild:
	docker build -t oc-lettings . && \
	docker rm -f oc-lettings 2>/dev/null || true && \
	docker run -d --name oc-lettings -p 8000:8000 oc-lettings
