from BaseEnv import BaseEnv

class AdaptiveMarketing(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.products = self.parameters.get("products", [
            {"id": "p1", "name": "Product 1", "display_quantity": 10},
            {"id": "p2", "name": "Product 2", "display_quantity": 5}
        ])
        self.videos = self.parameters.get("videos", ["v1", "v2"])
        self.data_sources = self.parameters.get("data_sources", ["default_source"])

    def analyze_trends(self, *, data_source):
        if not isinstance(data_source, str) or not data_source:
            return {"success": False, "message": "Invalid data_source."}
        if data_source not in self.data_sources:
            return {"success": False, "message": f"Data source '{data_source}' not found."}
        # Simulate trend analysis
        return {
            "success": True,
            "data": {
                "summary": f"Trends for {data_source}: mock trend data."
            }
        }

    def list_products(self):
        return {
            "success": True,
            "data": {
                "products": self.products
            }
        }

    def update_display_quantity(self, *, product_id, new_quantity):
        if not isinstance(product_id, str) or not product_id:
            return {"success": False, "message": "Invalid product_id."}
        if not isinstance(new_quantity, int) or new_quantity < 0:
            return {"success": False, "message": "new_quantity must be a non-negative integer."}
        for product in self.products:
            if product["id"] == product_id:
                product["display_quantity"] = new_quantity
                return {"success": True, "message": f"Display quantity for {product_id} updated to {new_quantity}."}
        return {"success": False, "message": f"Product '{product_id}' not found."}

    def get_videos(self):
        return {
            "success": True,
            "data": {
                "videos": self.videos
            }
        }

    def upload_video(self, *, video_id):
        if not isinstance(video_id, str) or not video_id:
            return {"success": False, "message": "Invalid video_id."}
        if video_id in self.videos:
            return {"success": False, "message": f"Video '{video_id}' already exists."}
        self.videos.append(video_id)
        return {"success": True, "message": f"Video '{video_id}' uploaded successfully."}