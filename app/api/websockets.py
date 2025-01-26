from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Set, Dict, Any
import json
from datetime import datetime

from app.core.config import settings
from app.services.services import vehicle_service
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


async def verify_api_key(websocket: WebSocket) -> None:
    """Verify API key from query parameters."""
    api_key = websocket.query_params.get("api_key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


async def handle_websocket_connection(websocket: WebSocket):
    """Handle WebSocket connection for real-time vehicle search."""
    try:
        # Verify API key before accepting connection
        await verify_api_key(websocket)
        
        # Check connection limit
        if (
            hasattr(websocket.app.state, "websocket_connections") and
            len(websocket.app.state.websocket_connections) >= settings.MAX_WEBSOCKET_CONNECTIONS
        ):
            await websocket.close(code=1008)  # Policy Violation
            return
        
        # Accept connection
        await websocket.accept()
        
        # Add to active connections
        if not hasattr(websocket.app.state, "websocket_connections"):
            websocket.app.state.websocket_connections = set()
        websocket.app.state.websocket_connections.add(websocket)
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                
                # Validate message type
                if "type" not in data or data["type"] != "search":
                    await websocket.send_json({
                        "type": "error",
                        "code": "INVALID_MESSAGE_TYPE",
                        "message": "Invalid message type"
                    })
                    continue
                
                # Validate search term
                search_term = data.get("search_term", "")
                if len(search_term) < 2:
                    await websocket.send_json({
                        "type": "error",
                        "code": "INVALID_SEARCH",
                        "message": "Search term must be at least 2 characters"
                    })
                    continue
                
                # Perform search
                db = SessionLocal()
                try:
                    vehicles, _ = vehicle_service.search_vehicles(
                        db,
                        search_term,
                        skip=0,
                        limit=10
                    )
                    
                    # Send results
                    await websocket.send_json({
                        "type": "search_results",
                        "results": [
                            {
                                "number_plate": v.number_plate,
                                "contact_name": v.contact_name,
                                "phone_number": v.phone_number,
                                "entry_timestamp": v.entry_timestamp.isoformat()
                            }
                            for v in vehicles
                        ],
                        "timestamp": datetime.utcnow().isoformat()
                    })
                finally:
                    db.close()
                
        except WebSocketDisconnect:
            pass
        finally:
            # Remove from active connections
            if hasattr(websocket.app.state, "websocket_connections"):
                websocket.app.state.websocket_connections.discard(websocket)
    
    except HTTPException as e:
        await websocket.close(code=1008, reason=e.detail)
    except Exception as e:
        await websocket.close(code=1011)  # Internal Error
    finally:
        # Ensure connection is closed
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()