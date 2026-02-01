"""
Content model for managing text content with IDs.
"""
from dataclasses import dataclass, field


@dataclass
class Content:
    """
    Model class for content with ID and text.
    
    Attributes:
        id: Unique identifier for the content item (e.g., URL, article ID, or UUID)
        text: The full text content of the article or document
    """
    id: str = field(metadata={"description": "Unique identifier for the content item"})
    text: str = field(metadata={"description": "Full text content of the article or document"})
    
    def to_dict(self) -> dict:
        """Convert content to dictionary format."""
        return {
            "id": self.id,
            "text": self.text
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Content':
        """Create Content instance from dictionary."""
        return cls(
            id=data["id"],
            text=data["text"]
        )

