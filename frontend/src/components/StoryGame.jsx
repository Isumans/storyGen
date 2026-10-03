import {useState, useEffect} from 'react';

function StoryGame({story, onNewStory}) {
    const [currentNodeId, setCurrentNodeId] = useState(null);
    const [currentNode, setCurrentNode] = useState(null);
    const [options, setOptions] = useState([]);
    const [isEnding, setIsEnding] = useState(false);
    const [isWinningEnding, setIsWinningEnding] = useState(false);

    useEffect(() => {
        if (story && story.root_node) {
            const rootNodeId = story.root_node.id
            setCurrentNodeId(rootNodeId);
        }
    }, [story]);

    useEffect(() => {
        if (currentNodeId && story && story.all_nodes ) {
            const node =story.all_nodes[currentNodeId];
            setCurrentNode(node);
            setIsEnding(node.is_ending);
            setIsWinningEnding(node.is_winning_ending);
            
            if(!node.is_ending && node.options && node.options.length > 0){
                setOptions(node.options);
            }else{
                setOptions([]);
            }
        }
    }, [currentNodeId, story]);

    const chooseOption = (optionId) =>{
        setCurrentNodeId(optionId);
    }
    const restartStory = () => {
        if(story && story.root_node){
            setCurrentNodeId(story.root_node.id);
        }
    }

    return <div className="story-game"> 
        <header>
            <h1>{story.title}</h1>
        </header>

        <div className="story-content">
            {currentNode && <div className="story-node">
                <p>{currentNode.content}</p>
            </div>}
            {isEnding ?
                <div className="story-ending">
                    <h3>{isWinningEnding ? "You Win!" : "Game Over"}</h3>
                    {isWinningEnding ? "Congratulations! You've reached a winning ending." : "Sorry, you've reached a losing ending."}
                </div>
                : 
                <div className="story-options">
                    <h3>What do you want to do?</h3>
                    <div className="options-list">
                        {options.map((option) =>{
                            return <button 
                                    key={option.node_id} 
                                    className="option-btn"
                                    onClick={() => chooseOption(option.node_id)}>{option.text}
                                    </button>
                        })}
                    </div>
                </div>
            }
        </div>
        <div className="story-controls">
            <button className="reset-btn" onClick={restartStory}>Restart Story</button>
        </div>
        {onNewStory && <button onClick={onNewStory} className="new-story-btn">Create New Story</button>}
    </div>

}
export default StoryGame;