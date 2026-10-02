function LoadingStatus({theme}){
    return <div className={`loading-container`}>
        <h2>Generating your {theme} story...</h2>

        <div className="loading-animation">
            <div className="loading-spinner"></div>
        </div>

        <p className="loading-info">
            This may take a few seconds. Please wait...
        </p>
    </div>
}