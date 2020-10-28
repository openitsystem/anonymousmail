// 获取邮箱列表
export function getEmailsStorage() {
    let infoValue = JSON.parse(localStorage.getItem('emails'));
    if (infoValue){
        if (infoValue['mailList'].length !== 0){
            return infoValue
        }
    }
    const info = {"mailList":[generateMixed(5)+"@mfk.app"]}
    setEmailsStorage('emails',info)
    return info
}

export function setEmailsStorage(name,info) {
    localStorage.setItem(name, JSON.stringify(info));
    return true
}


export function addEmailsStorage(mailAddress) {
    const mailAddressValue = mailAddress.toLowerCase()
    let infoValue = JSON.parse(localStorage.getItem('emails'));
    if (infoValue){
        if (infoValue['mailList'].length !== 0){
            if((infoValue['mailList']).indexOf(mailAddressValue+"@mfk.app")==-1){ //等于-1表示这个字符串中没有o这个字符
                infoValue['mailList'].push(mailAddressValue+"@mfk.app")
                setEmailsStorage('emails',infoValue)
            }else{
                setEmailsStorage('emails',infoValue)
            }
            return true
        } else {
            infoValue['mailList'].push(mailAddressValue+"@mfk.app")
            setEmailsStorage('emails',infoValue)
        }
        return true
    }
    const info = {"mailList":[mailAddressValue+"@mfk.app"]}
    setEmailsStorage('emails',info)
    return true
}

export function removeEmailsStorage(name) {
    let infoValue = JSON.parse(localStorage.getItem('emails'));
    if (infoValue){
        if (infoValue['mailList']){
            let index = (infoValue['mailList']).indexOf(name);
            if (index > -1) {
                (infoValue['mailList']).splice(index, 1);
            }
            setEmailsStorage('emails',infoValue)
            return true
        }
    }
    return true
}
export function removeAllEmailsStorage() {
    const info = {"mailList":[]}
    setEmailsStorage('emails',info)
    return true
}

export function generateMixed(n) {
    const chars = ['a','b','c','d','e','f','g','h','i','j','k','m','n','p','q','r','t','u','v','w','x','y'];
    let res = "";
    for(let i = 0; i < n ; i ++) {
        let id = Math.ceil(Math.random()*21);
        res += chars[id];
    }
    return res;
}